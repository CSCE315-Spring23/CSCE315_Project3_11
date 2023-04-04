from django.test import TestCase
import json
from pos.models import Employee
from pos.models import MenuItem

# Create your tests here.
employee1 = Employee.objects.get(EmployeeID=1)
print(employee1.FirstName)

menu_items = MenuItem.objects.all()
for item in menu_items:
    print(item.ItemName)
