from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee, Department
from django.contrib.auth.models import User
from .serializers import EmployeeSerializer, DepartmentSerializer, UserSerializer,SignupSerializer, LoginSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
# Create your views here.

#create SignupAPIView(APIVIEW):

class SignupAPIView(APIView):
    permission_classes = [AllowAny] #Signup does not need logging in
    
    #defining post fn to handle singup post data
    def post(self,request):
        #create an object for the SignupSerializer()
        #by giving the data received to its constructor
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():

            #create a new user if the serializer is valid
            user = serializer.save() #will give back a user object
            #after creating the user ,create a token  for the user
            token, created = Token.objects.get_or_create(user=user) #will give back token obj
             #once the user is created , give back the response with usrid,usrname,token,group
            return Response({
            "userid": user.id,
            "username": user.username,
            "token" :token.key,
            "role": user.groups.all()[0].id if user .groups.exists() else None
            #give back the first role id of the user if the role/group exists
            }, status=status.HTTP_201_CREATED)
        else:
            response = {'status':status.HTTP_400_BAD_REQUEST,' data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny] #Signup does not need logging in
    
    #defining post fn to handle singup post data
    def post(self,request):
        #create an object for the SignupSerializer()
        #by giving the data received to its constructor
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request, username=username, password=password)
            if user is not None:
                token=Token.objects.get(user=user)
                response = {
                    "status":"sucess",
                    "username": user.username,
                    "role":user.groups.all()[0].id if user.groups.exists() else None,
                    "data":{
                        "Token",token.key
                    }
                }
                return Response(response, status=status.HTTP_200_OK) 
            else:
                response = {
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid username or password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED) #login failed
            response = {'status':status.HTTP_400_BAD_REQUEST,' data':serializer.errors}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)  

#create viewset cls inheriting the Modelviewset class


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all() #get all objects of the model
    serializer_class = DepartmentSerializer #and render it using this serilalizer
    #permission_classes = [ ] #to bypass the authentication
    permission_classes = [IsAuthenticated] # to restrict for login users
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all() #get all objects of the model
    serializer_class = EmployeeSerializer #and render it using this serilalizer
    filter_backends = [filters.SearchFilter] #create a search filter
    search_fileds = ['EmployeeName' , 'Designation'] #add the fields to search
    permission_classes = [] #to bypass the authentication
    #permission_classes = [IsAuthenticated] # to restrict for login users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() #get all objects of the model
    serializer_class = UserSerializer #and render it using this serilalizer        

