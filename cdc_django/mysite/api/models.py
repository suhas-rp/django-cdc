from django.db import models

# Create your models here.
class student(models.Model):
    id = models.CharField(max_length=30)
    rollno = models.CharField(max_length=30,primary_key=True)
    batch = models.IntegerField()
    branch = models.CharField(max_length=30)
    #create student class to set fields and relations

class placement(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    ctc = models.FloatField()
    #create placement class to set fields and relations

class placementApplication(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    placement = models.ForeignKey(placement, on_delete=models.CASCADE)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    selected = models.BooleanField()
    #create placementapplication class to set fields and relations between placement and students

    def __str__(self):
        return self.title