from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    

   path('add_Program',views.add_Program,name="add_Program" ),
   path('add_Module/<int:ProgramId>',views.add_Module, name="add_Module"),
   path('add_Group/<int:ProgramId>', views.add_Group, name="add_Group"),
   
   path('update_Program/<int:ProgramId>',views.update_Program, name="update_Program"),
   path('program_Details/<int:ProgramId>',views.program_Details, name="program_Details"),
   path('update_Module/<int:ModuleId>', views.update_Module, name="update_Module"),
   path('module_Details/<int:ModuleId>', views.module_Details, name="module_Details"),
   path('delete_group/<int:GroupId>', views.delete_group, name="delete_group"),
   path('done_Group_Adding/<int:ProgramId>', views.done_Group_Adding, name="done_Group_Adding"),
   path('Group_Details/<int:GroupId>', views.Group_Details, name="Group_Details"),
   path('module_Select_Group/<int:ModuleId>', views.module_Select_Group, name="module_Select_Group"),
   path('Assign_Lecture/<int:moduleId>', views.Assign_Lecture, name="Assign_Lecture"),
   path('UserDetail/<str:email>', views.UserDetail, name="UserDetail"),
   path("assignExisting", views.assignExisting, name="assignExisting"),
   path('all_Programs', views.all_Programs, name="all_Programs"),
   path('all_Modules/<int:ProgramId>', views.all_Modules, name="all_Modules"),
   path('all_Groups/<int:ProgramId>', views.all_Groups, name="all_Groups"),
   path('all_Lectures/<int:ProgramId>',views.all_Lectures, name="all_Lectures")
   
   
   
]
