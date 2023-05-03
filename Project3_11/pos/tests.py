import os
import time

from django.conf import settings
from django.test import TestCase
import json

import pos.inventoryFunctions
from datetime import datetime
from pos.models import *
from pos.inventoryFunctions import *
from pos.reportFunctions import *
from django.utils import timezone
from pos.menu_functions import *

# Print the name of an Employee given their ID
# employee1 = Employee.objects.get(EmployeeID=1)
# print(employee1.FirstName)

# Change the price of a MenuItem given its name
# bowl_item = MenuItem.objects.get(ItemName="Bowl")
# bowl_item.Price = 9.99
# bowl_item.save() # Updates the database with the new value

# Getting the full menu
# full_menu = MenuItem.objects.all()
# for item in full_menu:
#     print(item.ItemName + " costs " + str(item.Price))

# Adding a new item to the menu
# add_to_menu("Smoothie", 4.69, ["Cup Drink", "Straw", "Cup Lid"], ["Spinach", "Dr. Pepper", "Diet Pepsi"])

# Placing an order
# custom_item1 = MenuItem.objects.get(ItemName="Bowl")
# custom_item1.select_items(["Spinach", "Brown Rice", "Cucumbers", "Greek Vinaigrette"])
# custom_item2 = MenuItem.objects.get(ItemName="Fountain Drink")
# custom_item2.select_items(["Gatorade"])
# order_items = [custom_item1, custom_item2]
# new_order = Order(EmployeeID=employee1.EmployeeID)
# new_order.add_to_order(order_items)
# new_order.save()

# find an inventory item info by name
# item_dict = findInventoryItem("Spinach")
# print(item_dict["Stock"])

# add an inventory item, specify whichever fields you want - the others will be put to null values
# addInventoryItem(name="Test", order_chance=0.5)

# remove an inventory item by name
# removeInventoryItem("Test")

# sales report given two dates
# start_date = timezone.make_aware(datetime(2022, 3, 1, 0, 0), timezone.get_current_timezone())
# end_date = timezone.make_aware(datetime(2022, 3, 3, 0, 0), timezone.get_current_timezone())
#
# items, counts, total = generateSalesReport(start_date, end_date)
# print(items)
# print(counts)
# print(total)

# sql command to check functionality (total is messed up)
# SELECT SUM("Total") AS total_sales, JSONB_ARRAY_ELEMENTS("MenuItemsInOrder") AS item, COUNT(*) AS item_count FROM "Orders" WHERE "DateTimePlaced" BETWEEN '2022-03-01' AND '2022-03-03' GROUP BY item;
# sql command to check total:
# select sum("Total") as total from "Orders" where "DateTimePlaced" Between '2022-03-01' and '2022-03-03';

# print("sales report total:", total)
# print("items:", items)
# print("counts:", counts)

# print("X report:", generateXReport())

# generateZReport()

# restock_report = generateRestockReport(3)
# for i in range(len(restock_report)):
#     print(restock_report[i].Name)

# excess_report = generateExcessReport(timezone.make_aware(datetime.datetime(2023, 2, 25, 0, 0), timezone.get_current_timezone()))
# for i in range(len(excess_report)):
#     print(excess_report[i].Name)

# start_date = timezone.make_aware(datetime.datetime(2022, 4, 1, 0, 0), timezone.get_current_timezone())
# end_date = timezone.make_aware(datetime.datetime(2022, 4, 4, 0, 0), timezone.get_current_timezone())
# pairs = whatSalesTogether(start_date, end_date)
# print(pairs)

#---------------------------------------------------------------
# Weather API stuff
# uses Anthony's API key so don't run until we find a workaround

# from bs4 import BeautifulSoup
# import requests
#
# APIURLcurrent = r"https://api.openweathermap.org/data/2.5/weather?lat=30.627979&lon=-96.334412&appid=b564f1dbb4cd614c0ee84abe3f4c820c&units=imperial&mode=xml"
# r = requests.get(APIURLcurrent)
# content = BeautifulSoup(r.content, features="xml")
#
# bigSectionTemp = content.findAll('temperature')
# bigSectionWeather = content.findAll('weather')
#
# for element in bigSectionWeather:
#     print(element.get('value'))
#
# for element in bigSectionTemp:
#     print(element.get('value'))
#---------------------------------------------------------------

# --------------------------------------------------------------
# Encoding images to base64 and creating SQL commands to update the database
# items = InventoryItem.objects.all()
# with open ("pos/images/update_inventory_pictures.sql", "w") as sql_file:
#     for item in items:
#         item_image_file = "pos/images/Default Image.png"
#         if os.path.isfile("pos/images/output/" + item.Name + ".png"):
#             item_image_file = "pos/images/output/" + item.Name + ".png"
#         with open(item_image_file, "rb") as image_file:
#             image_str = str(base64.b64encode(image_file.read()))
#             image_str = image_str[2:len(image_str) - 1]
#             out_line = "UPDATE \"InventoryItems\" SET \"Image\" = '" + image_str + "' WHERE \"Name\" = '" + item.Name + "';\n"
#             sql_file.write(out_line)
#             print(out_line)
# menu_items = MenuItem.objects.all()
# with open ("pos/images/update_menu_pictures.sql", "w") as sql_file:
#     for item in menu_items:
#         item_image_file = "pos/images/Default Image.png"
#         if os.path.isfile("pos/images/output/" + item.ItemName + ".png"):
#             item_image_file = "pos/images/output/" + item.ItemName + ".png"
#         with open(item_image_file, "rb") as image_file:
#             image_str = str(base64.b64encode(image_file.read()))
#             image_str = image_str[2:len(image_str) - 1]
#             out_line = "UPDATE \"MenuItems\" SET \"Image\" = '" + image_str + "' WHERE \"ItemName\" = '" + item.ItemName + "';\n"
#             sql_file.write(out_line)
#             print(out_line)
# --------------------------------------------------------------

# from google.cloud import translate_v2 as translate
# client = translate.Client(credentials=settings.CREDENTIALS)
# menu_items = MenuItem.objects.all()
# start = time.time()
# for item in menu_items:
#     item.ItemName = client.translate(item.ItemName, target_language="es")["translatedText"]
# end = time.time()
# print("Translation time:", end - start)

# from google.cloud import translate_v2 as translate
# import time
#
# client = translate.Client(credentials=settings.CREDENTIALS)
#
# # Split menu items into batches of 100 (or less)
# batch_size = 100
# menu_items = MenuItem.objects.all()
# num_batches = (len(menu_items) + batch_size - 1) // batch_size
#
# start = time.time()
#
# for i in range(num_batches):
#     # Get a batch of menu items
#     batch_start = i * batch_size
#     batch_end = min(batch_start + batch_size, len(menu_items))
#     batch_items = menu_items[batch_start:batch_end]
#
#     # Get a list of item names to be translated
#     item_names = [item.ItemName for item in batch_items]
#
#     # Translate the item names
#     translations = client.translate(item_names, target_language="es")
#
#     # Update the menu items with the translated names
#     for j, item in enumerate(batch_items):
#         item.ItemName = translations[j]["translatedText"]
#
# end = time.time()
#
# print("Translation time:", end - start)


