from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.decorators import gzip
import face_recognition
import cv2
import os
import pickle
import numpy as np
import cvzone
from datetime import date, datetime
from management.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from management.views import countobj
from .serializers import *


def home(request):
    
    if request.user.is_authenticated == True:
        
        if request.user.is_staff == True and request.user.is_superuser == False:
            lecture = get_object_or_404(Lecture, user = request.user)
            
            return redirect("lectur_deshboad", LectureId = lecture.LectureId)
            pass
        
        
        try:
            
            student = get_object_or_404(Student, user = request.user)
            print("Home try 2: ",student)
            if student.Program == None:
                messages.info(request, "Please update you details most importantly the selection of the program.")
                return redirect("Add_Student", StudentId = student.StudentId)
            else:
                if student.Group == None:
                    messages.info(request, "Please select a group that you were assigned to.")
                    return redirect("select_Group", StudentId=student.StudentId)
                if student.StudentNumber == '':
                    messages.info(request, "Please add your student number")
                    return redirect("Add_Student", StudentId = student.StudentId)
            print("student found " )
            return redirect("student_deshboad", GroupId=student.Group.GroupId,StudentId =student.StudentId)
        except:
            pass
    
    return render(request, 'streamApp/home.html')
class VideoCamera:
    def __init__(self):
        encodingFile = open('encdogindWithImageIds.p', 'rb')
        encdogindWithImageIds = pickle.load(encodingFile)
        self.student = None 
        self.iclass = None
        self.request = None
        encodingFile.close()
        self.encodeListKnown,self.imageIdList = encdogindWithImageIds
        
        print("we got the codes!")
       
        self.video = cv2.VideoCapture(0)  # 0 for the default camera (you can change it if needed)

    def __del__(self):
        self.video.release()
    
   
    def setfaceloc(self,facelocation):
        self.faceloc = facelocation
    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return b''
        self.success,self.image = success, image
        #smallImage = cv2.resize(image,(0,0),None,0.25,0.25)
        smallImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.faceOnFrame = face_recognition.face_locations(smallImage)
        self.faceEncodings = face_recognition.face_encodings(smallImage,self.faceOnFrame)
        
        
        for  encodeFace,faceloc in zip(self.faceEncodings,self.faceOnFrame):
           
            top, right, bottom, left = faceloc
            bbox = (left, top, right - left, bottom - top)
            cvzone.cornerRect(image,bbox,rt=0) 
            
            matchingFace = face_recognition.compare_faces(self.encodeListKnown,encodeFace)
            faceDistance = face_recognition.face_distance(self.encodeListKnown,encodeFace)
            matchIndex = np.argmin(faceDistance)
            if matchingFace[matchIndex]:
                
                
                
                self.student = get_object_or_404(Student, rootImageText = f"streamApp/images/{self.imageIdList[matchIndex]}")
                
                print("known face detected!", self.student.first_name+" "+ self.student.last_name)
            else:
                try:
                        mode = get_object_or_404(TheMdes, Class = self.iclass)    
                except:
                    mode = TheMdes.objects.create(
                        Message = "Face does not match any student on the database, deny access!",
                        Class = self.iclass,
                    )
                    
                    
        
        
        _, frame = cv2.imencode('.jpg', image)
        return frame.tobytes()
   
# Decorator to enable Gzip compression for the video stream 
@gzip.gzip_page
def video_feed(request,  classId):
    #print("day: ",type(datetime.now().isoweekday()))
    return StreamingHttpResponse(stream('Attendence',request, classId), content_type="multipart/x-mixed-replace;boundary=frame")

def stream(Action, request,classId):
    camera = VideoCamera()
   
    Iclass = get_object_or_404(Class, pk = classId)
    camera.iclass = Iclass
    camera.request = request
    while True:
        frame = camera.get_frame() 
        if camera.student:
            if Iclass.Group == camera.student.Group:
                try:
                    attendance = get_object_or_404( Attendee,Class = Iclass, Student=camera.student )  
                    print("attendance: ", attendance)
                    print("Already marked")
                   
                   
                    
                    try:
                        mode = get_object_or_404(TheMdes, Class = Iclass)    
                    except:
                        mode = TheMdes.objects.create(
                            Message = "Already marked attendance for "+ attendance.Student.first_name+" "+attendance.Student.last_name,
                            Class = Iclass,
                            StudentId = attendance.Student,
                            StudentName = attendance.Student.first_name,
                            StudentSurname = attendance.Student.last_name,
                            type = 'danger'
                        )       
                except:
                    attendance = Attendee.objects.create(
                        Class = Iclass,
                        Student = camera.student    
                    )
                    try:
                        mode = get_object_or_404(TheMdes, Class = Iclass)    
                    except:
                        mode = TheMdes.objects.create(
                            Message = "Attendance marked",
                            Class = Iclass,
                            StudentId = attendance.Student,
                            StudentName = attendance.Student.first_name,
                        )
            else:
                try:
                    mode = get_object_or_404(TheMdes, Class = Iclass)    
                except:
                    mode = TheMdes.objects.create(
                        Message = "Student("+camera.student.StudentNumber+") does not belong to group "+Iclass.Group.GroupCode+", deny access!",
                        Class = Iclass,
                        StudentId = camera.student,
                        StudentName = camera.student.first_name,
                        StudentSurname = camera.student.last_name
                    ) 
            
               
            
            print("student: ", camera.student) 
            print("Iclass: ",Iclass)
        else:
            print("NO student")  
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')







def stream2():
    camera = VideoCamera()

    while True:
        frame = camera.get_frame()

        smallImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faceOnFrame = face_recognition.face_locations(smallImage)
        faceEncodings = face_recognition.face_encodings(smallImage, faceOnFrame)

        for encodeFace, faceloc in zip(faceEncodings, faceOnFrame):
            matchingFace = face_recognition.compare_faces(camera.encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(camera.encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDistance)

            top, right, bottom, left = faceloc
            bbox = (left, top, right, bottom)

            if matchingFace[matchIndex]:
                cvzone.cornerRect(frame, bbox, rt=0)

        # Encode the frame as JPEG for streaming
        _, jpeg_frame = cv2.imencode('.jpg', frame)
        frame_data = jpeg_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        
        

    
    
       
@login_required
def take_attendance(request, classId):
    
    iclass = get_object_or_404(Class, pk = classId)
    
    if iclass.Status == 'Pending':
        
        iclass.Status = 'Taking'
        iclass.Date = datetime.now()
        iclass.save()
    domain =get_current_site(request).domain
    
    if request.method == 'GET':
        attendees = Attendee.objects.filter(Class = iclass)
        informationOBJ = {
            "class":iclass,
            "attendees":attendees,
            "domain":domain
        }
        return render(request, 'streamApp/take_attendance.html', informationOBJ)
    

    
    
    
@api_view(['POST', 'GET'])
@login_required
def get_Attendees(request, classID):
    iclass = get_object_or_404(Class , pk = classID)
    
    attendees = Attendee.objects.filter(Class = iclass)
    numAttendees = countobj(attendees)

    
    
    informationOBJ = {
        "numAttendees":numAttendees,
      
    }
    return Response(informationOBJ)

@api_view(['POST', 'GET'])
def allAttendees(request,classID):

    iclass = get_object_or_404(Class , pk = classID)
    attendents = []
    Students = []
    attendees = Attendee.objects.filter(Class = iclass)
    for attendee in attendees:
        Students.append(attendee.Student)
        attendentOBJ = {
            "name": attendee.Student.first_name,
            "lastName": attendee.Student.last_name,
            "studentNumber": attendee.Student.StudentNumber,
            "StudentIamge":attendee.Student.StudentIamge
        }
    
	#tasks = Task.objects.filter(user=user).order_by('-id')
    serializer = StudentSerializer(Students, many=True)
	#taskTest = Task.objects.all(user = user)

    return Response(serializer.data)
@api_view(['POST', 'GET'])
def allCampusAttendees(request):

    
    attendents = []
    Students = []
    attendees = CompusAttendee.objects.filter(datecreated = date.today())
    for attendee in attendees:
        Students.append(attendee.Student)
        attendentOBJ = {
            "name": attendee.Student.first_name,
            "lastName": attendee.Student.last_name,
            "studentNumber": attendee.Student.StudentNumber,
            "StudentIamge":attendee.Student.StudentIamge
        }
    
	#tasks = Task.objects.filter(user=user).order_by('-id')
    serializer = StudentSerializer(Students, many=True)
	#taskTest = Task.objects.all(user = user)

    return Response(serializer.data)

@api_view(['POST', 'GET'])
def getMessages(request, classId):
    iclass = get_object_or_404(Class,pk = classId)
    mode = TheMdes()
    
    try:
        mode = get_object_or_404(TheMdes, Class = iclass)
        
    except:
        pass
    
    
    serializer = TheMdesSerializer(mode, many=False)
    
    return Response(serializer.data)


@api_view(['POST', 'GET'])
def getGateMessages(request):
   
    mode = TheGateMdes()
    
    try:
        modes = TheGateMdes.objects.filter(datecreated = date.today())
        
    except:
        pass
    
    
    serializer = TheMdesSerializer(modes, many=True)
    
    return Response(serializer.data)

@api_view(['POST', 'GET'])
def removeGateMode(request):
   
   
    modes = TheGateMdes.objects.filter(datecreated = date.today())
    for mode in modes:
        mode.delete()
    
    return Response({"status":"removed"})




@api_view(['POST', 'GET'])
def removeMode(request, classId):
    iclass = get_object_or_404(Class,pk = classId)
    mode = get_object_or_404(TheMdes, Class = iclass)
    
    mode.delete()
    
    return Response({"status":"removed"})


@login_required 
def Done_attendance(request, classId):
    Iclass = get_object_or_404(Class, pk = classId)
    Iclass.Status = "Complete"
    
    Iclass.save()
    
    messages.success(request, "class attendance taken successfully.")
    
    return redirect("lectur_deshboad", LectureId = Iclass.TimetableSlot.Lecture.LectureId)
    
    


