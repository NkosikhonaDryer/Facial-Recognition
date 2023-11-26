from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from decimal import Decimal
import random
from django.contrib.auth.models import User
from mailApp.views import *
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *



    

@login_required
def add_Program(request):

    
   
    if request.method == 'GET':  
       return render(request, 'management/add_Program.html')
   
    if request.method == 'POST':   
        program = Program.objects.create(
                
                ProgramName = request.POST["ProgramName"],
                ProgramCode = request.POST["ProgramCode"],
                AddedBy = request.user
            
            
        )
        messages.success(request, "Module added please add groups of students")
        #return redirect("add_Module",ProgramId = program.ProgramId)
        return redirect("add_Group", ProgramId = program.ProgramId)


@login_required
def add_Group(request, ProgramId):
    
    program = get_object_or_404(Program, pk = ProgramId)
    groups = Group.objects.filter(Program = program)
    
    if request.method == 'GET':
        
        return render(request, 'management/add_Group.html',{"Program":program,"groups":groups})
    
    if request.method == 'POST':
        program = get_object_or_404(Program, pk = int(request.POST["ProgramId"]))
        
        Sgroup = Group.objects.filter(Program = program, GroupCode = request.POST["GroupCode"])
        if Sgroup:
            messages.error(request, "A group with the same code on this modeule has already been created")
            return redirect("add_Group", ProgramId = program.ProgramId)
        
            
        group = Group.objects.create(
                    Program = program,
                    GroupCode = request.POST["GroupCode"], 
                    numStudents = 0
                )
        program.numGroups += 1
        program.save()
            
        messages.success(request,f'Group {group.GroupCode} Add successfully you may add more or hit "Done" if you are.')
        return redirect("add_Group", ProgramId = program.ProgramId)
             

@login_required
def update_Program(request,ProgramId):
    
    program = get_object_or_404(Program, pk =ProgramId)
    
    if request.method == 'GET':
        
        return render(request, 'management/update_Program.html', {"program":program})  
    
    if request.method == 'POST':
        
        numUpdate = 0
        if program.ProgramName != request.POST["ProgramName"]:
            
            program.ProgramName = request.POST["ProgramName"]
            numUpdate += 1
            
        if program.ProgramCode != request.POST["ProgramCode"]:
            program.ProgramCode = request.POST["ProgramCode"]
            numUpdate += 1
            
        if numUpdate > 0 :
            program.save()
            messages.success(request, "Changes saved successfully")
        else:
            messages.info(request, "No changes made.")
            
        return redirect("all_Programs")  
        
            
    
@login_required
def program_Details(request,ProgramId):
    
    program = get_object_or_404(Program, pk = ProgramId)
    
    return render(request, 'management/program_Details.html', {"program":program})
        

#"add_Module",ProgramId
@login_required
def add_Module(request,ProgramId):
    
    program = get_object_or_404(Program, pk = ProgramId)
    ms = Module.objects.filter(Program = program)
    modules = []
    for module in ms:
        print(countobj(ModuleGroup.objects.filter(Module = module)))
        obj = {
            "module":module,
            "groups": ModuleGroup.objects.filter(Module = module),
            "numGroup":countobj(ModuleGroup.objects.filter(Module = module))
        }
        modules.append(obj)
    
    if request.method == 'GET':
        
        return render(request, 'management/add_Module.html', {"program":program, "modules":modules})
    
    if request.method == 'POST':
        
        module = Module.objects.create(
            Program = program,
            AddedBy = request.user,
            ModuleName = request.POST["ModuleName"],
            ModuleCode = request.POST["ModuleCode"],
            
        )
        messages.success(request, "Module basic information added please add groups of students and assign lectures to groups")
        program.numModules += 1
        program.save()
        return redirect("module_Select_Group",ModuleId=module.ModuleId)
        
@login_required
def module_Select_Group(request, ModuleId):
    module = get_object_or_404(Module, pk = ModuleId)
    Program = module.Program
    groups = Group.objects.filter(Program = Program)
    if request.method == 'GET':
                
        return render(request, 'management/module_Select_Group.html', {"module":module,"Program":Program, "groups":groups})

    if request.method == 'POST':
        print("Request: ", request)
        numGroups =0
        for group in  groups:
            
            try:
                
                if request.POST[str(group.GroupCode)] == group.GroupCode:
                    try:
                        get_object_or_404(ModuleGroup,Module = module,Group =  group)    
                    except:
                        moduleGroup = ModuleGroup.objects.create(
                            Module = module,
                            Group = group
                        )
                    numGroups += 1
            except:
                pass
            
        print("numGroups: ",numGroups)
        if numGroups == 0:
            messages.error(request, "PLease select at least on  group to take on the module.")
        messages.success(request, "Groups have been selectes successfully please assign a lecture to each group")
        return redirect("Assign_Lecture", moduleId=module.ModuleId)
   
@login_required
def Assign_Lecture(request, moduleId):
    
    module = get_object_or_404(Module, pk = moduleId)
    print("module: ",module)
    groups =[]
    moduleGroups = ModuleGroup.objects.filter(Module = module, Lecture = None)
    print("moduleGroups: ",moduleGroups)
    for group in moduleGroups:
        groups.append(group.Group)
    program = module.Program
    Lectures = []
    ls = Lecture.objects.filter(Program = program)
    for l in ls:
        obj = {
            "Lecture": l,
            "moduleGroups": ModuleGroup.objects.filter(Module = module, Lecture = l)
            
        }
        Lectures.append(obj)
        
        
   
    
    
    if request.method =='GET':
        
        print("groups: ", groups)
            
        return render(request, 'management/Add_Lecture.html', {"moduleGroups":moduleGroups,"Program":program,"groups":groups, "Lectures":Lectures,"ProgramLectures":ls})
    
    if request.method =='POST':
        is_userExist = False
        userPassword = None
        try:
            LectureUser = get_object_or_404(User, email = request.POST['email'].lower())
            is_userExist = True
        except:
            userPassword = generate_New_Password()
            LectureUser = User.objects.create_user(
                first_name = request.POST["first_name"],
                last_name = request.POST["last_name"],
                username = request.POST['email'].lower(),
                email =request.POST['email'].lower(), 
                password = userPassword,
                is_active = True,
                is_staff = True
                )
        
        
        lecture = Lecture.objects.create(
            Program = program,
            user = get_object_or_404(User, email = request.POST['email'].lower()),
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            
            email =request.POST['email'].lower(), 
            PhoneNumber = request.POST["PhoneNumber"],
            numGroups = 0
        )
        moduleGroup = get_object_or_404(ModuleGroup, pk = int(request.POST["ModuleGroupId"]))
        lecture.numGroups += 1
        moduleGroup.Lecture = lecture
        moduleGroup.save()
        lecture.save()
        moduleGroups = ModuleGroup.objects.filter(Module = module, Lecture = None)
        LectureActivationEmail(request,LectureUser,request.POST['email'].lower(),moduleGroup.ModuleGroupId,userPassword, is_userExist)
        
        count =  len(moduleGroups)
        if countobj(moduleGroups) > 0:
            
            messages.success(request, f"{lecture.first_name} {lecture.last_name} has been assigned to group {moduleGroup.Group.GroupCode} for {moduleGroup.Module.ModuleName}")
            return redirect("Assign_Lecture",moduleId = module.ModuleId )
        else:
            messages.success(request, f"Lectures have been assigned to all groups and to the module({module.ModuleCode}) successfully, you may add more modules.") 
            return redirect("add_Module",ProgramId = program.ProgramId)
    
def assignExisting(request):
    
    if request.method  == 'POST':
        moduleGroup = get_object_or_404(ModuleGroup, pk = request.POST["moduleGroupId"])
        lecture = get_object_or_404(Lecture, pk = request.POST["LectureId"])
        
        lecture.numGroups += 1
        moduleGroup.Lecture = lecture
        moduleGroup.save()
        lecture.save()  
        
        
    moduleGroups = ModuleGroup.objects.filter(Module = moduleGroup.Module, Lecture = None)
    is_userExist = True
    userPassword = None
    if countobj(moduleGroups) > 0:
            
        messages.success(request, f"{lecture.first_name} {lecture.last_name} has been assigned to group {moduleGroup.Group.GroupCode} for {moduleGroup.Module.ModuleName}")
        LectureActivationEmail(request,lecture.user,lecture.email,moduleGroup.ModuleGroupId,userPassword, is_userExist)
        return redirect("Assign_Lecture",moduleId = moduleGroup.Module.ModuleId )
    else:
        messages.success(request, f"Lectures have been assigned to all groups and to the module({moduleGroup.Module.ModuleCode}) successfully, you may add more modules.") 
        return redirect("add_Module",ProgramId = moduleGroup.Module.Program.ProgramId)
    
     
@api_view(['GET'])
def UserDetail(request, email):
	user = get_object_or_404(User, email = email)
	serializer = UserSerializer(user, many=False)
	return Response(serializer.data)

    
@login_required
def update_Module(request, ModuleId ):
    module = get_object_or_404(Module, pk = ModuleId)
    
    if request.method =='GET':
        
        return render(request, 'management/update_Module.html', {"module":module})
    
    if request.method =='POST':
        
        numUpdate = 0
        if module.ModuleName != request.POST["ModuleName"]:
           module.ModuleName = request.POST["ModuleName"]
           numUpdate += 1
        if module.ModuleCode != request.POST["ModuleCode"]:
            module.ModuleCode = request.POST["ModuleCode"]
            numUpdate += 1
            
        if numUpdate > 0:
            module.save()
            messages.success(request, "Changes saved suucessfully")
        else:
            messages.info(request, "No changes made.")
        
        return redirect("module_Details", ModuleId=module.ModuleId )
    
@login_required
def module_Details(request,ModuleId):
    
    module = get_object_or_404(Module, pk = ModuleId)
    groups = ModuleGroup.objects.filter(Module = module)
    return render(request, 'management/module_Details.html', {"module":module, "groups":groups})
            

@login_required
def Group_Details(request, GroupId):
    
    group = get_object_or_404(Group, pk =GroupId )
    program = group.Program
    modules = ModuleGroup.objects.filter(Group = group)
    numModules = countobj(modules)
    students = Student.objects.filter(Group = group)
    numStudents = countobj(students)
    return render(request, 'management/Group_Details.html', {"program":program,"group":group, "modules":modules,"students":students, "numModules":numModules, "numStudents":numStudents })
    
def all_Groups(request, ProgramId):
    program = get_object_or_404(Program, pk =ProgramId )
    
    groups = Group.objects.filter(Program = program)
    
    return render(request, 'management/all_Groups.html', {"groups":groups,"program":program})       
  
@login_required
def delete_group(request, GroupId):
    group = get_object_or_404(Group, pk = GroupId)
    groupModule = ModuleGroup.objects.filter(Group =group )
    for module in groupModule:
        module.Group = None
        module.save()
    grpCode = group.GroupCode
    program = group.Program
    program.numGroups -= 1
    program.save()
    group.delete()
    
    messages.success(request, f"Group '{grpCode}' has been deleted")
    
    return redirect("add_Group",ProgramId = program.ProgramId)   
        
        
def done_Group_Adding(request, ProgramId):
    
    program = get_object_or_404(Program, pk =ProgramId )
  
    program.Status = "Active"
    program.save()
    
    messages.success(request, "Program student groups, please add modules for this program")

   # messages.success(request, f"{module.ModuleName} modeule with {module.numGroups} groups was created successfully. You may continue adding modules for the program.")
    
    
    return redirect("add_Module", ProgramId= program.ProgramId)
    
    
def countobj(list):
    count = 0
    for i in list:
        count += 1
    return count
    
    
    
def generate_New_Password():
    specialCharecters = '!@#$%&*()[]'#11
    alphabets ='abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    password = ''
    
    for i in range(0,4,1):
     
        Schar = specialCharecters[random.randint(0, 10)] 
        alpha =  alphabets[random.randint(0, 25)]
        num = numbers[random.randint(0, 9)]
        
        for j in range(1,3,1):
            type = random.randint(1, 3)
            if type == 1:
                password += Schar+alpha+num
            elif type == 2:
                password += alpha+Schar+num
            else:
                password += num+alpha+Schar
    
    return password   



def all_Programs(request):
    
    ps = Program.objects.all()
    programs = []
    for program in ps:
        obj={
            "program":program,
            "numModules": countobj(Module.objects.filter(Program = program))
        }
        programs.append(obj)
    if request.method =='GET':
        
        return render(request, 'management/all_Programs.html' ,{"programs":programs})

def all_Modules(request, ProgramId):
    
    program = get_object_or_404(Program, pk = ProgramId)
    ms = Module.objects.filter(Program = program)
    modules = []
    for module in ms:
        print(countobj(ModuleGroup.objects.filter(Module = module)))
        obj = {
            "module":module,
            "groups": ModuleGroup.objects.filter(Module = module),
            "numGroup":countobj(ModuleGroup.objects.filter(Module = module))
        }
        modules.append(obj)
        
    return render(request, 'management/all_Modules.html', {"program":program, "modules":modules})


@login_required
def all_Lectures(request, ProgramId):
    
    program = get_object_or_404(Program, pk = ProgramId) 
    programNumModules = countobj(Module.objects.filter(Program = program))
    all_Program_Modules = Module.objects.filter(Program = program)
    
    for module in all_Program_Modules:
        
        pass
    NoGroupModule = 0
    
    Ls = Lecture.objects.filter(Program = program)
    lectures = []
    for lecture in Ls:
        obj = {
            "Lecture":lecture,
            "groups": ModuleGroup.objects.filter(Lecture = lecture),
            "numGroups": countobj(ModuleGroup.objects.filter(Lecture = lecture))
            
        }
        lectures.append(obj)
         
    
    return render(request, 'management/all_Lectures.html',{"program":program,"Lectures":lectures, "programNumModules":programNumModules})
    