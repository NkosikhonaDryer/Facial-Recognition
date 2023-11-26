from rest_framework import serializers
from management.models import *
from django.contrib import messages

class AttendeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Attendee
		fields ='__all__'
  
class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields ='__all__'
  
class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields ='__all__'
  
class TheMdesSerializer(serializers.ModelSerializer):
	class Meta:
		model = TheMdes
		fields ='__all__'
  
class TheGateMdesSerializer(serializers.ModelSerializer):
	class Meta:
		model = TheGateMdes
		fields ='__all__'
  
  
class CompusAttendeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompusAttendee
		fields ='__all__'
  
