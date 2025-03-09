from rest_framework import serializers
from .models import student,placement,placementApplication

#serializers to convert django data to python data types

class studentserializer(serializers.ModelSerializer):
    class Meta:
        model = student
        fields = ["id","rollno","batch","branch"]
        
class placementserializer(serializers.ModelSerializer):
    class Meta:
        model = placement
        fields = ['id','name','role','ctc']

class placementApplicationserailizer(serializers.ModelSerializer):
    class Meta:
        model = placementApplication
        fields = ['id','placementid','studentid','selected']