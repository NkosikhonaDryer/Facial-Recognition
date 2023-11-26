from django.db import models
from datetime import date, datetime, time
from django.contrib.auth.models import User 

# Create your models here.

# class Order(models.Model):
#     OrderId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
#     user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#Customer



  
class Program(models.Model):
    AddedBy = models.ForeignKey(User,blank=True,null=True,on_delete=models.DO_NOTHING)
    ProgramId =  models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    ProgramName = models.CharField(max_length=150, null=False, blank=False)
    ProgramCode = models.CharField(max_length=20, null=False, blank=False)
    numGroups = models.IntegerField(default=0)
    numModules = models.IntegerField(default=1)
    DateCreated = models.DateTimeField(default=datetime.now())
    Status = models.CharField(max_length=30, default='Available')
    
    
class Module(models.Model):
    ModuleId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    Program = models.ForeignKey(Program,blank=True,null=True,on_delete=models.DO_NOTHING)
    AddedBy = models.ForeignKey(User,blank=True,null=True,on_delete=models.DO_NOTHING)
    ModuleName = models.CharField(max_length=150, null=False, blank=False)
    ModuleCode = models.CharField(max_length=20)
    numGroups = models.IntegerField(default=0)
    Status = models.CharField(max_length=20,default='OnCreate')
    DateCreated = models.DateTimeField(default=datetime.now())
 
class Group(models.Model):
    GroupId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    
    Program = models.ForeignKey(Program,blank=True,null=True,on_delete=models.DO_NOTHING)
   
    
    GroupCode = models.CharField(max_length=5, null=False, blank=False)
    numStudents = models.IntegerField(default=1)
    
    status = models.CharField(max_length=30, default='Active')
    DateCreated = models.DateTimeField(default=datetime.now())
class Lecture(models.Model):
    LectureId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.DO_NOTHING)#Lecture user account
    Program = models.ForeignKey(Program,blank=True,null=True,on_delete=models.DO_NOTHING)
    
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email  = models.CharField(max_length=150, blank=False, null=False)
    numGroups = models.IntegerField(default=1)
    PhoneNumber = models.CharField(max_length=15, default='+27')
class ModuleGroup(models.Model):
    ModuleGroupId =  models.AutoField(primary_key=True,blank=False, null=False,auto_created=True) 
    Module = models.ForeignKey(Module,blank=True,null=True,on_delete=models.DO_NOTHING)
    Group = models.ForeignKey(Group,blank=True,null=True,on_delete=models.DO_NOTHING)
    Lecture = models.ForeignKey(Lecture,blank=True,null=True,on_delete=models.DO_NOTHING)
    
class Student(models.Model):
    StudentId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#Student user account
    Group = models.ForeignKey(Group,blank=True,null=True,on_delete=models.DO_NOTHING)
    Program = models.ForeignKey(Program,blank=True,null=True,on_delete=models.DO_NOTHING)
    
    StudentNumber = models.CharField(max_length=20, blank=True, null = True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email  = models.CharField(max_length=150, blank=False, null=False)
    PhoneNumber = models.CharField(max_length=15, default='+27')
    StudentIamge = models.FileField(blank=True,null=True,upload_to='streamApp/images')
    TempLink = models.CharField(max_length=500, null=True, blank=True )
    numModules = models.IntegerField(blank=True, null=True)
    AttendanceRate = models.DecimalField(blank=False, null=False,max_digits=20,decimal_places=2)
    Status = models.CharField(max_length=20,default='Oncreate')
    rootImageText = models.CharField(max_length=600, null=True, blank=True)



class TimetableSlot(models.Model):
    SlotId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    Lecture = models.ForeignKey(Lecture,blank=True,null=True,on_delete=models.DO_NOTHING)
    ModuleGroup = models.ForeignKey(ModuleGroup,blank=True,null=True,on_delete=models.DO_NOTHING)
    
    weekdayNum = models.IntegerField(blank=False, null=False)# Monday == 1 and Sunday == 7
    Time = models.TimeField()
    #EndTime = models.TimeField(default=datetime.time())
    weekday = models.TextField()
    
    Venue = models.TextField(null=True, blank=True)
    
    def getweekday(numday):
        
        numDay = numday
        weekday = 'Monday'
        if numDay == 1:
            pass
        elif numDay == 2:
            weekday = 'Tuesday'
        elif numDay == 3:
            weekday = 'Wednesday'
        elif numDay == 4:
            weekday = 'Thursday'
        elif numDay == 5:
            weekday = 'Friday'
        elif numDay == 6:
            weekday = 'Saturday'
        elif numDay == 7:
            weekday = 'Sunday'
            
        return weekday
           
    
    
class Class(models.Model):
    ClassId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    Group = models.ForeignKey(Group,blank=True,null=True,on_delete=models.DO_NOTHING)
    
    TimetableSlot = models.ForeignKey(TimetableSlot,blank=True,null=True,on_delete=models.DO_NOTHING)    
    Status = models.CharField(max_length=20, default='Pending')
    Date = models.DateTimeField(default=datetime.now())
   
     
class Attendee(models.Model):
    AttendeeId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    Class = models.ForeignKey(Class,blank=True,null=True,on_delete=models.DO_NOTHING)
    Student = models.ForeignKey(Student,blank=True,null=True,on_delete=models.DO_NOTHING)
    

class TheMdes(models.Model):
    currentAttendee = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    Class = models.ForeignKey(Class,blank=True,null=True,on_delete=models.DO_NOTHING)
    StudentName = models.TextField(null=True, blank=True)
    StudentSurname = models.TextField(null=True, blank=True)
    
    StudentId = models.ForeignKey(Student,blank=True,null=True,on_delete=models.DO_NOTHING)
    Message = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, default='success')
    
class TheGateMdes(models.Model):
    currentAttendee = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    
    StudentName = models.TextField(null=True, blank=True)
    StudentSurname = models.TextField(null=True, blank=True)
    Student = models.ForeignKey(Student,blank=True,null=True,on_delete=models.DO_NOTHING)
    Message = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, default='success')
    
    datecreated = models.DateField(default=date.today())

class Security(models.Model):
    
    SecurityId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#Student user account
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email  = models.CharField(max_length=150, blank=False, null=False)
    PhoneNumber = models.CharField(max_length=15, default='+27')
    Keeperimage = models.FileField(blank=True,null=True,upload_to='streamApp/images')
    rootImageText = models.CharField(max_length=600, null=True, blank=True)
    status = models.CharField(max_length=50, default="Active")
    datecreated = models.DateField(default=datetime.now())
    

class CompusAttendee(models.Model):
    
    CompusAttendeeId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    takenBy = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#Student user account
    Student = models.ForeignKey(Student,blank=True,null=True,on_delete=models.DO_NOTHING)
    
    datecreated = models.DateField(default=date.today())
    dateTimeCreated =models.DateTimeField(default=datetime.now())
            
            
    
    
    

    
class StudentGroup(models.Model):
    
    StudentGroupId = models.AutoField(primary_key=True,blank=False, null=False,auto_created=True)
    Group = models.ForeignKey(Group,blank=True,null=True,on_delete=models.DO_NOTHING)
    Student = models.ForeignKey(Student,blank=True,null=True,on_delete=models.DO_NOTHING)
    numClasses = models.IntegerField(blank=True, null=True)
    numClassAttended = models.IntegerField(blank=True, null=True)
    
    
    
    
    
    
    
    
    
    
    