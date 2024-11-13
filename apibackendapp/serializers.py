from rest_framework import serializers
from .models import Employee,Department
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.ModelSerializer):
    #we will receiving username ,password and groupname
    #at first take the group_name save it in a variable,then
    #remove it from the list so that we can create new user
    group_name = serializers.CharField(write_only=True, required=False)
    #write only means the field will be used for input
    
    #function to create the user
    def create(self, validated_data):
        #at first remove the group_name from the validated_data
        #so tht we have only username and password to create the user
      group_name = validated_data.pop("group_name", None)
        #as part of the security , encrypt the password and save it
      validated_data['password'] = make_password(validated_data.get("password"))
      #create the user using the validated_data containing username and password
      user = super(SignupSerializer, self).create(validated_data)
      #now we can add  the created user to the group
      if group_name:
        group, created = Group.objects.get_or_create(name=group_name)
        #attepting create group object with the specified group name if not exists
        user.groups.add(group) #add the user to that group
        return user #return the newly created user
    class Meta:
        model = User
        fields = ['username','password','group_name']

class LoginSerializer(serializers.ModelSerializer):
    #creating the custom filed for username
    username = serializers.CharField()
    class Meta:
        model= User
        fields = ['username','password']


#create serializer by inheriting Modelserializer class
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta: #will provide meta data to model
        model = Department
        fields = ('DepartmentId', 'DepartmentName')
       
def name_validation(employee_name):
    if len(employee_name)<3:
        raise serializers.ValidationError("Name must be atleast 3 chars")
    return employee_name
class EmployeeSerializer(serializers.ModelSerializer ):
    Department = DepartmentSerializer(source ='DepartmentId', read_only=True)
    EmployeeName = serializers.CharField(max_length=200 , validators=[name_validation])
    class Meta:
        model = Employee
        fields=('EmployeeId','EmployeeName','Designation','DateOfJoining','IsActive','DepartmentId','Department')
class UserSerializer(serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = ('id','username') #get only these two fields

                        