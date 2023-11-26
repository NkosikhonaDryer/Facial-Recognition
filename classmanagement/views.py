
from management.models import *
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.models import User
from streamApp.EncodingGenerator import *
import face_recognition
import numpy as np
import cv2
import os
from django.core.files import File
from django.conf import settings
from datetime import date, datetime
from management.views import countobj

import cv2
import face_recognition
import pickle
import os



@login_required
def Add_Student(request, StudentId):
    
    student = get_object_or_404(Student,StudentId = StudentId )
    user = request.user
    programs = Program.objects.all()
    if request.method == 'GET':
        try:
            print(findEncodings2())
        except:
            pass
        return render(request, 'classmanagement/Add_Student.html', {"programs":programs, "student":student})
    
    if request.method =='POST':
        numUpdates = 0
        isImageUpdate = False
        if student.StudentNumber != request.POST["StudentNumber"]:
            student.StudentNumber = request.POST["StudentNumber"]
            numUpdates +=1
        
        if student.first_name != request.POST["first_name"]:
            student.first_name = request.POST["first_name"]
            numUpdates += 1
            
        if student.last_name != request.POST["last_name"]:
            student.last_name = request.POST["last_name"]
            numUpdates+=1
        
        if student.email != request.POST["email"]:
            
            student.email = request.POST["email"]
            numUpdates+=1
            
        if student.PhoneNumber != request.POST["PhoneNumber"]:
            
            student.PhoneNumber = request.POST["PhoneNumber"]
            numUpdates+=1
            
        try:
            if student.StudentIamge:
                delete_file_from_field(student,"StudentIamge")
            student.StudentIamge = request.FILES["studentImage"]
                
            #student.TempLink = rename_and_get_uploaded_image(student.StudentNumber,  request.FILES["StudentIamge"])
            print(student.StudentIamge)
            
            isImageUpdate = True
            numUpdates+=1
        except:
            pass
        
        
        if student.Program == None:
            student.Program = get_object_or_404(Program, pk = request.POST["ProgramId"])
            numUpdates+=1
            
        
        if numUpdates >0:
            student.save()
            if isImageUpdate == True:
                print("Plit text: ",os.path.splitext(student.StudentIamge.name))
                
                root, ext = os.path.splitext(student.StudentIamge.name)
                student.rootImageText = root
                student.save()
                
            messages.success(request, "Changes saved successfully")
        else:
            messages.error(request, "No changes made.")
        # if isImageUpdate:  
        #     isFaceFound = findFace(request.FILES["StudentIamge"])
        #     if isFaceFound:
        #         print("Face found")
                
        if student.Group == None:
            messages.info(request, "Please select a group that you were assigned to.")
            return redirect("select_Group", StudentId= student.StudentId)
            
        else:
            messages.error(request,"NO face detected on you image please make sure you have clear view of your face on the image.")
            return redirect("Add_Student",StudentId = student.StudentId )
            
def createStudent(user):
    student = Student.objects.create(
            user = user,
            
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
    
            
            numModules = 0,
            AttendanceRate =0.00,
            
                  
        )
    return student
@login_required
def select_Group(request, StudentId):
    
    student = get_object_or_404(Student, pk = StudentId)
    program = student.Program
    groups = Group.objects.filter(Program = program)
    
    if request.method == 'GET':
        
        return render(request, 'classmanagement/select_Group.html', {"student":student, "program":program, "groups":groups}) 
    
    if request.method == 'POST':
        
        group = get_object_or_404(Group, pk = request.POST["GroupId"])
        student.Group = group
        group.numStudents +=1
        group.save()
        student.save()
        
        messages.success(request, "you have seleceted group \""+group.GroupCode+"\" as your group, please see below your modules.")
        return redirect("student_deshboad", GroupId = group.GroupId, StudentId = student.StudentId)
        
              

@login_required
def student_deshboad(request, GroupId, StudentId):
    group = get_object_or_404(Group, pk = GroupId)
    student = get_object_or_404(Student, pk = StudentId)
    
    program = group.Program
    ms = ModuleGroup.objects.filter(Group = group)
    modules = []
    todayTimetableSlot = []
    isWeekEnd = False
    dayToday = datetime.now().isoweekday()
    if dayToday == 6 or dayToday == 7:
        isWeekEnd = True
        
    for module in ms:
        timetableSlots = TimetableSlot.objects.filter(ModuleGroup = module)
        
        numClass = 0
        NumAttended = 0
        attendanceRate = 0.00
        
    
        
        for slot in timetableSlots:
            if slot.weekdayNum == dayToday:
                todayTimetableSlot.append(slot)
            numClass += countobj(Class.objects.filter(TimetableSlot = slot, Status='Complete'))
            theClasses=Class.objects.filter(TimetableSlot = slot, Status='Complete')
            for classE in theClasses:
                NumAttended += countobj(Attendee.objects.filter(Student = student, Class =classE ))
             
        try:
            attendanceRate = (NumAttended/numClass)*100
        except:
            pass   
        obj = {
            "moduleGroup":module,
            "timetableSlots":timetableSlots,
            "attendanceRate":attendanceRate
        } 
        modules.append(obj)
    print("todayTimetableSlot: ",todayTimetableSlot)
    informationOBJ = {
        "group":group,
        "student":student,
        "program":program,
        "modules":modules,
        "todayTimetableSlots":todayTimetableSlot,
        "isWeekEnd":isWeekEnd,
        "attendanceRate":attendanceRate
        
        
    }    
    
    return render(request, 'classmanagement/student_deshboad.html',informationOBJ )
    
@login_required
def lectur_deshboad(request, LectureId):
    lecture = get_object_or_404(Lecture, pk = LectureId)
    ms = ModuleGroup.objects.filter(Lecture = lecture)
    moduleGroups =[] 
    classes = []
    todaySlots = []
    for m in ms:
        timetableSlots = TimetableSlot.objects.filter(ModuleGroup = m).order_by('-Time')
        numClassConducted = 0
        for timetableSlot in timetableSlots:
            if timetableSlot.weekdayNum == datetime.now().isoweekday():
                todaySlots.append(timetableSlot)
            classess = Class.objects.filter(TimetableSlot =timetableSlot )
            numClassConducted += countobj(classes)
            for Iclass in classess:
                #classes object
                objCalss = {
                    
                    "timetableSlot":timetableSlot,
                    "class":Iclass, 
                }
                classes.append(objCalss)
        #moduleGroups object  
        numStudents = countobj(Student.objects.filter(Group = m.Group))
        obj = {
            "moduleGroup":m,
            "timetableSlots": timetableSlots,
            "numClassConducted":numClassConducted ,
            "numStudents":numStudents
            
        }
        moduleGroups.append(obj)
        
    todayClasses = []
    if todaySlots:
        for todaySlot in todaySlots:
            try:
                oClass = get_object_or_404(Class,TimetableSlot =todaySlot,Status='Pending')
                todayClasses.append(oClass)
            except:
                
                iclass = Class.objects.create(
                    Group = todaySlot.ModuleGroup.Group,
                    TimetableSlot = todaySlot,
                ) 
                todayClasses.append(iclass)
        
    informationOBJ = {
        "moduleGroups":moduleGroups,
        "classes":classes,
        "lecture":lecture,
        "todayClasses":todayClasses
        
        
    }
    
    return render(request, 'classmanagement/lectur_deshboad.html',informationOBJ)
@login_required  
def group_module_deshboad(request, ModuleGroupId):
    
    moduleGroup = get_object_or_404(ModuleGroup, pk = ModuleGroupId)
    timetableSlots = TimetableSlot.objects.filter(ModuleGroup =moduleGroup ).order_by('weekdayNum') 
    students = Student.objects.filter(Group = moduleGroup.Group)
    
    informationOBJ = {
        "moduleGroup":moduleGroup,
        "timetableSlots":timetableSlots,
        "students":students
    }
    
    return render(request, 'classmanagement/group_module_deshboad.html',informationOBJ)
  
@login_required
def add_TimeSlot(request, ModuleGroupId):
    moduleGroup = get_object_or_404(ModuleGroup,pk = ModuleGroupId)
    timetableSlots = TimetableSlot.objects.filter(ModuleGroup = moduleGroup).order_by("weekdayNum")
    
    if request.method == 'GET':
        print(time)
        return render(request,'classmanagement/add_TimeSlot.html', {"moduleGroup":moduleGroup,"timetableSlots":timetableSlots })
    
    if request.method == 'POST':
        try:
            
            slot =  get_object_or_404(TimetableSlot,Time = request.POST["Time"], Venue = request.POST["Venue"],weekdayNum = request.POST["weekdayNum"])
            messages.error(request, "The time slot you have added has been already taken, please try another.")
            return redirect("add_TimeSlot",ModuleGroupId=ModuleGroupId)
        except:
            pass
        
        
        print("time: ", request.POST["Time"])
        slot = TimetableSlot.objects.create(
            Lecture = moduleGroup.Lecture,
            ModuleGroup = moduleGroup,
            weekdayNum = request.POST["weekdayNum"],
            Time = request.POST["Time"],
            Venue = request.POST["Venue"],
            weekday = TimetableSlot.getweekday(int(request.POST["weekdayNum"]))
        )
        
        messages.success(request, "Slot created success fully you may create more")
        return redirect("add_TimeSlot",ModuleGroupId=ModuleGroupId)
     
@login_required
def module_deshboad(request, ModuleGroupId):
    user = request.user
    student = get_object_or_404(Student, user = user)
    moduleGroup = get_object_or_404(ModuleGroup, pk = ModuleGroupId)
    timetableSlots = TimetableSlot.objects.filter(ModuleGroup = moduleGroup)
    numClasses = countobj(Class.objects.filter(Group = moduleGroup.Group,  Status='Complete'))
    numClassesAttended = countobj(Attendee.objects.filter(Student = student))
    attendanceRate = 0.00
    try:
        attendanceRate = (numClassesAttended/numClasses)*100
    except:
        pass
    
    informationOBJ = {
        "moduleGroup":moduleGroup,
        "numClasses":numClasses,
        "numClassesAttended":numClassesAttended,
        "attendanceRate": attendanceRate,
        "student":student,
        "timetableSlots":timetableSlots
        
    }
    
    return render(request, 'classmanagement/module_deshboad.html',informationOBJ)
    
    
@login_required
def slot_Details(request, SlotId):
    
    slot = get_object_or_404(TimetableSlot, pk = SlotId)
    cls = Class.objects.filter(TimetableSlot = slot)
    classes = []
    
    for iclass in cls:
        numAttendees = countobj(Attendee.objects.filter(Class = iclass))
        classOBJ = {
            "class":iclass,
            "numAttendees":numAttendees
            
        }
        classes.append(classOBJ)
    infometioOBJ = {
        "slot":slot,
        "classes":classes,
        "numClasses":countobj(classes),
        "moduleGroup":slot.ModuleGroup,
    }
    
    return render(request, 'classmanagement/slot_Details.html',infometioOBJ)    
    


@login_required
def update_Slot(request, SlotId):
    
    slot = get_object_or_404(TimetableSlot, pk = SlotId)
    
    if request.method == 'GET':
        
        return render(request, 'classmanagement/update_Slot.html', {"slot":slot})
    
    if request.method == 'POST':
        
        numUpdates = 0
        
        if slot.weekdayNum != int(request.POST["weekdayNum"]):
            slot.weekdayNum = int(request.POST["weekdayNum"])
            slot.weekday = TimetableSlot.getweekday(slot.weekdayNum)
            numUpdates += 1
            
        if request.POST["Time"] !='':
            if slot.Time != request.POST["Time"]:
                slot.Time = request.POST["Time"]
                numUpdates += 1
                
            
        if slot.Venue != request.POST["Venue"]:
            
            slot.Venue = request.POST["Venue"]
            numUpdates += 1
           
            
        if numUpdates > 0:
            
            slot.save()
            messages.success(request, "Changes saved suuceesfully")
        else:
            messages.info(request, "NO chamges made")    
            
        return redirect("slot_Details",SlotId=slot.SlotId)
        
        
            
            
            
    
def findFace(image_file):
    isFaceFound = False

    try:
        # Read the image file using OpenCV
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        
        if image is not None:
            # Convert the image from BGR to RGB
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            print("image: ", img)
            
            # Perform face encoding using face_recognition library
            face_encodings = face_recognition.face_encodings(img)
            
            if face_encodings:
                isFaceFound = True
                encode = face_encodings[0]
                print("encoding: ", encode)

    except Exception as e:
        # Handle the exception (e.g., log the error)
        print("Error:", str(e))

    return isFaceFound

@login_required#ob=nly students
def group_Time_Table(request, GroupId):
    user = request.user
    student = get_object_or_404(Student, user =user )
    group = get_object_or_404(Group, pk = GroupId)
    modules = ModuleGroup.objects.filter(Group = group)
    
    Monday = [] 
    Tuesday = [] 
    
    Wednesday = [] 
    
    Thursday = [] 
    
    Friday = [] 
    
    Saturday = [] 
    
    Sunday = [] 
    
    #getting the slot for all the days
    
    for module in modules:
        
        timetableslots = TimetableSlot.objects.filter(ModuleGroup = module).order_by('Time')
        
        for slot in timetableslots:
            if slot.weekdayNum == 1:
                Monday.append(slot)
            if slot.weekdayNum == 2:
                Tuesday.append(slot)
            if slot.weekdayNum == 3:
                Wednesday.append(slot)
            if slot.weekdayNum == 4:
                Thursday.append(slot)
            if slot.weekdayNum == 5:
                Friday.append(slot)
            if slot.weekdayNum == 6:
                Saturday.append(slot)
            if slot.weekdayNum == 7:
                Sunday.append(slot)
                
    timetable = {
        "Monday":Monday,
        "Tuesday":Tuesday,
        "Wednesday":Wednesday,
        "Thursday":Thursday,
        "Friday":Friday,
        "Saturday":Saturday,
        "Sunday":Sunday
    }
    
    informationOBJ ={
        "student":student,
        "group":group,
        "timetable":timetable
    }
    
    return render(request, 'classmanagement/group_Time_Table.html', informationOBJ)
    
    

@login_required
def class_Attendees(request, classId):
    Iclass = get_object_or_404(Class, pk = classId)
    module = get_object_or_404(ModuleGroup, Group = Iclass.Group)
    attendees = Attendee.objects.filter(Class = Iclass)
    numAttendess = countobj(attendees)
    domain = get_current_site(request)
    
    informationOBJ = {
        "class":Iclass,
        "attendees":attendees,
        "module":module,
        "numAttendess":numAttendess,
        "domain":domain
    }
    
    return render(request, 'classmanagement/class_Attendees.html', informationOBJ)
   
   
   
@login_required
def group_students(request, moduleGroupId):
    domain = get_current_site(request)
    moduleGroup = get_object_or_404(ModuleGroup, pk =moduleGroupId )
    classes = Class.objects.filter(Group = moduleGroup.Group, Status = 'Complete')
  
    numClasses = countobj(classes)
    
    students = []
    
    studs = Student.objects.filter(Group = moduleGroup.Group)
    
    for student in studs:
        attendenceRate = 0.00
        numAttended = countobj(Attendee.objects.filter(Student = student))
        try:
            attendenceRate = (numAttended/numClasses)*100
        except:
            pass
        studentOBJ = {
            "student": student,
            "attendenceRate":attendenceRate
        }
        students.append(studentOBJ)
        
    informationOBJ = {
        "students":students,
        "moduleGroup":moduleGroup,
        "group":moduleGroup.Group,
        "module":moduleGroup.Module,
        "numStudents":countobj(students),
        "numClasses":numClasses,
        "domain":domain
       
    }
    
    return render(request, 'classmanagement/group_students.html', informationOBJ)
    
     
    
# def rename_and_get_uploaded_image(new_filename, file):
#     try:
#         # Get the uploaded image file from request.FILES
#         uploaded_image = file #request.FILES["StudentImage"]

#         # Construct the new file path with the desired filename and the appropriate file extension
#         _, file_extension = os.path.splitext(uploaded_image.name)
#         new_file_name = f"{new_filename}{file_extension}"
#         new_file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)
#         print("File path: ", new_file_path)
#         # Save the uploaded image with the new filename
#         with open(new_file_path, 'wb') as new_image_file:
#             for chunk in uploaded_image.chunks():
#                 new_image_file.write(chunk)

#         # Create a new File object for the renamed image
#         new_image = File(open(new_file_path, 'rb'))
#         print("new_image: ", new_image)
#         # Optionally, you can delete the original uploaded image if needed
#         # os.remove(uploaded_image.temporary_file_path())

#         # Return the new File object
#         return new_file_path

#     except Exception as e:
#         # Handle any exceptions (e.g., file write error)
#         print("Error:", str(e))
#         return None



def delete_file_from_field(instance, field_name):
    file_field = getattr(instance, field_name)
    
    if file_field:
        file_path = file_field.path
        
        if os.path.isfile(file_path):
            print("File found")
            os.remove(file_path)
        
        # Clear the file field
        setattr(instance, field_name, None)
        
        # Save the instance to update the database
        instance.save() 
        return True
    else:
        return False
    
    
    
    
def findEncodings2():
    #images = 'stramApp/images'
    print("Starting codings")
    images = 'media/streamApp/images'
    imagesPathList = os.listdir(images)

    imagesList =[]
    imageIdList = []

    
    for path in imagesPathList:
        imagesList.append(cv2.imread(os.path.join(images, path)))
        print("path: ",path)
        
        imageIdList.append(os.path.splitext(path)[0])
        
    
    encodingsList = []
    num =0
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]  
     
        num += 1
        encodingsList.append(encode)
    encodeListKnown = encodingsList
    encdogindWithImageIds = [encodeListKnown,imageIdList]
    file = open("encdogindWithImageIds.p","wb")
    pickle.dump(encdogindWithImageIds,file)
    file.close()
    print()
    print("coding end!")
    return encodingsList
