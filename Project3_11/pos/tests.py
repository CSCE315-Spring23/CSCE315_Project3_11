from django.test import TestCase

from pos.models import Employee

# Create your tests here.
employee1 = Employee.objects.get(EmployeeID=1)
print(employee1.FirstName)
