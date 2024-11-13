from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
# Create your wonderful models here.hello world
#create a department model class by inheriting the Model class
#create a receiver for the signal 'post_save' for the user model
#once its created create a Token for thet user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance) #create token for the user
       #create a department model class by inheriting the model Class 
class Department(models.Model):
    DepartmentId=models.AutoField(primary_key=True)

    DepartmentName=models.CharField(max_length=200)



    def __str__(self):
        return self.DepartmentName

class Employee(models.Model):
    EmployeeId=models.AutoField(primary_key=True)
    EmployeeName=models.CharField(max_length=200)
    Designation = models.CharField(max_length=150)
    DateOfJoining = models.DateField()
    DepartmentId = models.ForeignKey(Department,on_delete=models.CASCADE)
    Contact = models.CharField(max_length=150)                                 
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.EmployeeName       
