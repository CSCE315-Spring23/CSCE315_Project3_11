from django.test import TestCase
import json
from pos.models import Employee
from pos.models import MenuItem

# Print the name of an Employee given their ID
employee1 = Employee.objects.get(EmployeeID=1)
print(employee1.FirstName)

# Change the price of a MenuItem given its name
bowl_item = MenuItem.objects.get(ItemName="Bowl")
bowl_item.Price = 9.99
# bowl_item.save() # Updates the database with the new value

# Getting the full menu
full_menu = MenuItem.objects.all()
for item in full_menu:
    print(item.ItemName + " costs " + str(item.Price))
