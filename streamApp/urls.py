from django.urls import path
from . import views


urlpatterns = [
    path('video_feed/<int:classId>', views.video_feed, name='video_feed'),
    path('', views.home,name="home"),
    path('take_attendance/<int:classId>', views.take_attendance, name="take_attendance"),
    path('get_Attendees/<int:classID>', views.get_Attendees, name="get_Attendees"),
    path('allAttendees/<int:classID>', views.allAttendees, name="allAttendees"),
    path('getMessages/<int:classId>', views.getMessages, name="getMessages"),
    path('removeMode/<int:classId>',  views.removeMode, name="removeMode"),
    path('Done_attendance/<int:classId>', views.Done_attendance, name="Done_attendance"),
    path('getGateMessages', views.getGateMessages, name="getGateMessages"),
    path('removeGateMode', views.removeGateMode, name="removeGateMode"),
    path('allCampusAttendees', views.allCampusAttendees, name="allCampusAttendees")
     
]