from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from .models import Department,Employee
from datetime import date
from django.urls import reverse
from .serializers import EmployeeSerializer
from rest_framework import status

# Create your tests here.
#creating new empviewsettestcls inheriting the apitestcase cls
class EmployeeViewSetTest(APITestCase):
    #defining a function to set up some basic data for testing
    def setUp(self):
#create a sample department object
       self.department = Department.objects.create(DepartmentName ="HR")
#create a sample employee object ansd assign the department
       self.employee = Employee.objects.create(
            EmployeeName = "jackie chan",
            Designation= "kungfu master",
            DateOfJoining= date(2024 , 11 ,13),
            DepartmentId= self.department,
            Contact= "China",
            IsActive = True)

        #since we are testing API,we need to create an API client object
       self.client =APIClient()
#TEST CASE 1:Listing
    #defining function to test employee listing api/endpoint
    def test_employee_list(self):
        #the default reverse url for listing modelname-list
        url = reverse('employee-list')   
        response = self.client.get(url) #send the url and get the response

        #get all the employee objects of employee model
        employee = Employee.objects.all()
        #create a serializer object from employee serializer
        serializer = EmployeeSerializer(employee, many=True) #get all employees

        #check and compare the response against the setup data
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #check if status code is 200
        self.assertEqual(response.data , serializer.data)
        # check if serializer data matches the actual data format

  #TEST CASE 2:To get particular employee details
    #defining function to test employee listing api/endpoint
    def test_employee_details(self):
       #the default reverse url for details is modelname-detials
      #also provide the employee id as argument
        url =  reverse('employee-detail',args =[self.employee.EmployeeId]) 
        response = self.client.get(url) #send the url and get the response
        
        #create a serializer object from employee serializer using the setup data
        serializer = EmployeeSerializer(self .employee) #get employees details

        #check and compare the response against the setup data
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #check if status code is 200
        self.assertEqual(response.data , serializer.data)
        # check if serializer data matches the actual data format
      