from django.test import TestCase
import json

import pos.inventoryFunctions
from pos.models import Employee
from pos.models import MenuItem
from pos.inventoryFunctions import *
from pos.reportFunctions import *
from django.utils import timezone
import datetime


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

# find an inventory item info by name
item_dict = findInventoryItem("Spinach")
print(item_dict["Stock"])

# add an inventory item, specify whichever fields you want - the others will be put to null values
# addInventoryItem(name="Test", order_chance=0.5)

# remove an inventory item by name
# removeInventoryItem("Test")

# sales report given two dates
start_date = timezone.make_aware(datetime.datetime(2022, 3, 1, 0, 0), timezone.get_current_timezone())
end_date = timezone.make_aware(datetime.datetime(2022, 3, 3, 0, 0), timezone.get_current_timezone())

report = generateSalesReport(start_date, end_date)
print("sales report total:", report)

