from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
import os
from datetime import date, datetime
from management.views import countobj
import face_recognition
import numpy as np
import pickle
import cv2

import cvzone
from django.contrib.auth.models import User
from management.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators import gzip
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse

from management.views import generate_New_Password
from classmanagement.views import findEncodings2, delete_file_from_field
from streamApp.views import VideoCamera
from mailApp.views import KeeperActivationEmail


@login_required
def add_GateKeeper(request):
    user = request.user
    if user.is_superuser != True:
        messages.error(request, "You are not allowed to access that page!!")
        return redirect('home')
    
    if request.method == 'GET':
        print(findEncodings2())
        return render(request, 'campusAttendance/add_GateKeeper.html')
    
    if request.method =='POST':
        
         
        KeeperUserPAssword = generate_New_Password()
        KeeperUser = User.objects.create_user(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            username = request.POST['email'].lower(),
            email =request.POST['email'].lower(), 
            password = KeeperUserPAssword,
            is_active = True,
            is_staff = False
            ) 
        
        security = Security.objects.create(
            user =KeeperUser,
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            PhoneNumber= request.POST["PhoneNumber"],
            Keeperimage = request.FILES["Keeperimage"],
            email =request.POST['email'].lower(), 
            
        )
        root, ext = os.path.splitext(security.Keeperimage.name)
        security.rootImageText = root
        security.save()
        
        KeeperActivationEmail(request,KeeperUser,KeeperUser.email,KeeperUserPAssword)
        messages.success(request, "Gate keeper added successfully you may add more")
        return redirect("add_GateKeeper")
        

@login_required
def update_GateKeeper(request, keeperId):
    
    security = get_object_or_404(Security, pk = keeperId)
    
    if request.method =='GET':
        
        findEncodings2()
        
        return render(request, 'campusAttendance/update_GateKeeper.html', {"security":security})
    
    if request.method == 'POST':
        pass
        numUpdate = 0
    
        if security.first_name != request.POST["first_name"]:
            security.first_name = request.POST["first_name"]
            security.user.first_name = request.POST["first_name"]
            numUpdate += 1
            
        if security.last_name != request.POST["last_name"]:
            security.last_name = request.POST["last_name"]
            security.user.last_name = request.POST["last_name"]
            numUpdate += 1
            
        if security.PhoneNumber != request.POST["PhoneNumber"]:
            security.PhoneNumber = request.POST["PhoneNumber"]
            numUpdate += 1
            
        if security.email != request.POST['email'].lower():
            security.email = request.POST['email'].lower()
            security.user.email = request.POST['email'].lower()
            numUpdate += 1
          
          
        try:
            if request.FILES["Keeperimage"]:
                delete_file_from_field(security, "Keeperimage")
                security.Keeperimage = request.FILES["Keeperimage"]
                numUpdate += 1
            
            
        except:
            pass  
        if numUpdate > 0:
            
            security.save()
            security.user.save()
            messages.success(request, "Changes saved successfully.")
            
        else:
            messages.error(request, "No changes made.")
            
        return redirect("update_GateKeeper",keeperId = keeperId)
        #~numUpdates  = 0
        # finish this and handle the attendance!!!!!!!
     
@login_required
def keeper_Details(request, keeperId):
    
    security = get_object_or_404(Security, pk = keeperId)
    
    return render(request, 'campusAttendance/keeper_Details.html', {"security": security})
     
@login_required
def myInfo(request):
    
    user = request.user
    security = get_object_or_404(Security, user=user)
    return redirect("keeper_Details",keeperId = security.SecurityId)   
     
@api_view(['POST', 'GET'])
@login_required
def Is_Security(request):
    
    is_Security = False
 
    user = request.user
    try:
        security = get_object_or_404(Security, user = user)
        is_Security = True
    except:
        pass
    
    
    return Response({"is_Security": is_Security})

class GateVideoCamera:
    def __init__(self):
        encodingFile = open('encdogindWithImageIds.p', 'rb')
        encdogindWithImageIds = pickle.load(encodingFile)
        self.student = None 
        self.iclass = None
        self.request = None
        encodingFile.close()
        self.encodeListKnown,self.imageIdList = encdogindWithImageIds
        
        
       
        self.video = cv2.VideoCapture(1)  # 0 for the default camera (you can change it if needed)

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
                    mode = TheGateMdes.objects.create(
                        Message = "Face does not match any student on the database, deny access!",
                        Class = self.iclass,
                    )
                    
                    
        
        
        _, frame = cv2.imencode('.jpg', image)
        return frame.tobytes()
   


#taking attendance
@gzip.gzip_page
def Gate_video_feed(request):
    #print("day: ",type(datetime.now().isoweekday()))
    return StreamingHttpResponse(streamGate(), content_type="multipart/x-mixed-replace;boundary=frame")

def streamGate():
    camera = GateVideoCamera()
   
    while True:
        frame = camera.get_frame() 
        if camera.student:
           
            try:
                compusAttendee = get_object_or_404(CompusAttendee ,Student=camera.student )  
                 
                print("attendance: ", compusAttendee)
                print("Already marked")
                
                
                
                try:
                    mode = get_object_or_404(TheGateMdes, Student = camera.student)    
                except:
                    mode = TheGateMdes.objects.create(
                        Message = "Already marked attendance for "+  camera.student.first_name+" "+ camera.student.last_name,
                     
                        Student =  camera.student,
                        StudentName =  camera.student.first_name,
                        StudentSurname =  camera.student.last_name,
                        type = 'danger'
                    )       
            except:
                    compusAttendee = CompusAttendee.objects.create(
                        Student = camera.student,
                            
                    )
                    try:
                        mode = get_object_or_404(TheGateMdes, Student = camera.student)    
                    except:
                        mode = TheGateMdes.objects.create(
                            Message = "Attendance marked",
                           
                            Student = camera.student,
                            StudentName =  camera.student.first_name,
                            StudentSurname =  camera.student.last_name
                        )
            
            
               
            
            print("student: ", camera.student) 
          
        else:
            # try:
            #     mode = get_object_or_404(TheGateMdes, Student = camera.student)    
            # except:
            #     mode = TheGateMdes.objects.create(
            #         Message = "",
                    
            #         Student = camera.student,
            #         StudentName =  camera.student.first_name,
            #         StudentSurname =  camera.student.last_name
            #     )
            print("NO student")  
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')





@login_required
def take_gate_attendee(request):
    
    domain =get_current_site(request).domain
    if request.method == 'GET':
        compusAttendee = CompusAttendee.objects.filter(datecreated = date.today())
        informationOBJ = {
            
            "attendees":compusAttendee,
            "domain":domain
        }
        return render(request, 'campusAttendance/take_gate_attendee.html', informationOBJ)