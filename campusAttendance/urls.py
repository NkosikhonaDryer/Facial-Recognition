"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('add_GateKeeper', views.add_GateKeeper, name="add_GateKeeper"),
    path('Is_Security', views.Is_Security, name="Is_Security"),
    path('keeper_Details/<int:keeperId>', views.keeper_Details, name="keeper_Details"),
    path('update_GateKeeper/<int:keeperId>', views.update_GateKeeper, name="update_GateKeeper"),
    path('myInfo', views.myInfo, name="myInfo"),
    path('Gate_video_feed', views.Gate_video_feed, name="Gate_video_feed"),
    path('take_gate_attendee', views.take_gate_attendee, name="take_gate_attendee")
    
   
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
