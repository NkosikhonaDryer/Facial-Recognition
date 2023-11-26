from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('Add_Student/<int:StudentId>', views.Add_Student, name="Add_Student"),
    path('select_Group/<int:StudentId>', views.select_Group, name="select_Group"),
    path('student_deshboad/<int:GroupId>/<int:StudentId>', views.student_deshboad, name="student_deshboad"),
    path('module_deshboad/<int:ModuleGroupId>',views.module_deshboad, name="module_deshboad" ),
    path('lectur_deshboad/<int:LectureId>', views.lectur_deshboad, name="lectur_deshboad"),
    path("group_module_deshboad/<int:ModuleGroupId>", views.group_module_deshboad, name="group_module_deshboad"),
    path("add_TimeSlot/<int:ModuleGroupId>", views.add_TimeSlot, name="add_TimeSlot"),
    path('slot_Details/<int:SlotId>',views.slot_Details, name="slot_Details"),
    path('update_Slot/<int:SlotId>', views.update_Slot, name="update_Slot"),
    path('group_Time_Table/<int:GroupId>', views.group_Time_Table, name="group_Time_Table"),
    path('class_Attendees/<int:classId>', views.class_Attendees, name="class_Attendees"),
    path('group_students/<int:moduleGroupId>',views.group_students, name="group_students")
    
    
    
    
]