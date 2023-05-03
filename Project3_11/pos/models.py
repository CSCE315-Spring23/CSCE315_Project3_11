import base64
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import datetime
from datetime import timedelta
from decimal import Decimal
from pos.common_functions import get_category

"""
Module containing Django models for the restaurant management system.

Classes:

Employee: A model representing an employee.
ExpirationDate: A model representing the expiration date of an inventory item.
InventoryItem: A model representing an inventory item.
MenuItem: A model representing a menu item.
Order: A model representing an order.
OrderInProgress: A model representing an in-progress order.
"""

class Employee(models.Model):
    """
    A model representing an employee.
    Attributes:
    - EmployeeID: An integer representing the employee's ID.
    - LastName: A string representing the employee's last name.
    - FirstName: A string representing the employee's first name.
    - HireDate: A date representing the employee's hire date.
    - EmployeePIN: An integer representing the employee's PIN.
    - PositionTitle: A string representing the employee's position title.
    - Email: A string representing the employee's email address.
    - HoursWorked: A decimal representing the number of hours worked by the employee.

    Meta:
    - db_table: The name of the database table to use for this model.
    """
    EmployeeID = models.IntegerField(primary_key=True)
    LastName = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=50)
    HireDate = models.DateField()
    EmployeePIN = models.IntegerField()
    PositionTitle = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    HoursWorked = models.DecimalField(max_digits=28, decimal_places=2)

    class Meta:
        db_table = "Employees"


class ExpirationDate(models.Model):
    """
    A model representing the expiration date of an inventory item.
    Attributes:
    - UniqueID: An integer representing the unique ID of the expiration date.
    - ItemName: A string representing the name of the inventory item.
    - ExpirationDate: A datetime representing the expiration date.
    - RemainingServings: An integer representing the remaining servings of the inventory item.

    Meta:
    - db_table: The name of the database table to use for this model.
    """
    UniqueID = models.IntegerField(primary_key=True)
    ItemName = models.TextField()
    ExpirationDate = models.DateTimeField()
    RemainingServings = models.IntegerField()

    class Meta:
        db_table = "ExpirationDates"


class InventoryItem(models.Model):
    """
    A model representing an inventory item.
    Attributes:
    - Name: A string representing the name of the inventory item.
    - Stock: An integer representing the current stock of the inventory item.
    - NumberNeeded: An integer representing the number of items needed.
    - OrderChance: A decimal representing the chance of an item being ordered.
    - Units: A string representing the units of the inventory item.
    - Category: A string representing the category of the inventory item.
    - Servings: An integer representing the servings of the inventory item.
    - RestockCost: An integer representing the cost of restocking the inventory item.
    - Image: A binary field representing the image of the inventory item.

    Meta:
    - db_table: The name of the database table to use for this model.
    """
    Name = models.TextField(primary_key=True)
    Stock = models.IntegerField()
    NumberNeeded = models.IntegerField()
    OrderChance = models.DecimalField(max_digits=28, decimal_places=2)
    Units = models.TextField()
    Category = models.TextField()
    Servings = models.IntegerField()
    RestockCost = models.IntegerField()
    Image = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = "InventoryItems"

    def save(self, *args, **kwargs):
        self.Image = self.Image.encode('utf-8')
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Image = bytes(self.Image).decode('utf-8')

class MenuItem(models.Model):
    """
    A model representing a menu item.
    Attributes:

    -ItemName: A string representing the name of the menu item.
    -Price: A decimal representing the price of the menu item.
    -DefiniteItems: A list of strings representing the definite items included in the menu item.
    -PossibleItems: A list of strings representing the possible items that can be included in the menu item.
    -Image: A binary field representing the image of the menu item.
    -selected_items: An empty list to store the selected items.
    Methods:

    -select_items(selected_items): Updates the selected_items list with the given list of selected items.
    -update_categories(): Updates the categories list with the categories of the possible items by querying the InventoryItem model.
    -save(*args, **kwargs): Overrides the save method to update the categories and encode the Image field before saving.
    -init(*args, **kwargs): Overrides the init method to update the categories and decode the Image field.
    Meta:

    -db_table: The name of the database table to use for this model.
    """
    ItemName = models.TextField(primary_key=True)
    Price = models.DecimalField(max_digits=28, decimal_places=2)
    DefiniteItems = models.JSONField(default=list)
    PossibleItems = models.JSONField(default=list)
    Image = models.BinaryField(null=True, blank=True)
    selected_items = []

    class Meta:
        db_table = "MenuItems"

    def select_items(self, selected_items):
        self.selected_items = selected_items

    def update_categories(self):
        self.categories = []
        for possible_item in self.PossibleItems:
            try:
                inventory_item = InventoryItem.objects.get(Name=possible_item)
                category = inventory_item.Category
                if category not in self.categories:
                    self.categories.append(category)
            except ObjectDoesNotExist:
                print("Does not exist: " + possible_item)

    def save(self, *args, **kwargs):
        self.update_categories()
        self.Image = self.Image.encode('utf-8')
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_categories()
        self.Image = bytes(self.Image).decode('utf-8')


class Order(models.Model):
    """
    A model representing an order made by a customer or employee.
    Attributes:

    -DateTimePlaced: A DateTimeField representing the time the order was placed.
    -EmployeeID: An integer representing the ID of the employee who took the order.
    -Items: A JSONField representing the items in the order.
    -Subtotal: A decimal representing the subtotal of the order.
    -Total: A decimal representing the total cost of the order (subtotal + tax).
    -MenuItemsInOrder: A JSONField representing the menu items in the order.
    -order_items: A list of the menu items in the order.
    Meta:

    -db_table: The name of the database table to use for this model.
    """
    DateTimePlaced = models.DateTimeField(primary_key=True)
    EmployeeID = models.IntegerField(default=-1)
    Items = models.JSONField(default=list)
    Subtotal = models.DecimalField(max_digits=28, decimal_places=2, default=0)
    Total = models.DecimalField(max_digits=28, decimal_places=2, default=0)
    MenuItemsInOrder = models.JSONField(default=list)
    order_items = []

    class Meta:
        db_table = "Orders"

    def save(self, *args, **kwargs):
        # Set current datetime as primary key
        if not self.pk:
            utc_now = datetime.utcnow()
            central_offset = timedelta(hours=-5)  # UTC-5 for Central Time
            central_now = utc_now + central_offset
            central_now = central_now.replace(microsecond=0)  # remove decimal of seconds
            self.DateTimePlaced = central_now

        # Update InventoryItems/ExpirationDates table
        for item in self.Items:
            try:
                closest_item = ExpirationDate.objects.filter(ItemName=item).order_by('ExpirationDate').first()
                if closest_item:
                    closest_item.RemainingServings -= 1
                    if closest_item.RemainingServings == 0:
                        closest_item.delete()
                        try:
                            inventory_listing = InventoryItem.objects.get(Name=item)
                            inventory_listing.Stock -= 1
                        except ObjectDoesNotExist:
                            print("No inventory item found in InventoryItems with name%s\n" % item)
                else:
                    print("No item: %s in ExpirationDates\n" % item)
            except ObjectDoesNotExist:
                print("No inventory item found in ExpirationDates with name %s\n" % item)

        super().save(*args, **kwargs)

    def add_to_order(self, menu_items):
        for item in menu_items:
            self.Items += item.DefiniteItems
            self.Items += item.selected_items
            self.MenuItemsInOrder += [item.ItemName]
            self.Subtotal += Decimal(str(item.Price))
            self.order_items += [item]
        self.Total = (self.Subtotal * Decimal(str(1.0825))).quantize(Decimal('.01'))

    def clear_order(self):
        self.Items = []
        self.Subtotal = 0
        self.Total = 0
        self.MenuItemsInOrder = []
        self.order_items = []


class OrderInProgress(models.Model):
    """
    A model representing an order that is currently in progress.
    Attributes:
    - DateTimeStarted: A datetime field representing the date and time when the order was started.
    - EmployeeID: An integer representing the ID of the employee who started the order.
    - CustomizedItems: A JSON field representing the customized items in the order.
    - Subtotal: A decimal field representing the subtotal of the order.
    - Total: A decimal field representing the total cost of the order after tax.

    Meta:
    - db_table: The name of the database table to use for this model.
    """
    DateTimeStarted = models.DateTimeField(auto_now=True, primary_key=True)
    EmployeeID = models.IntegerField(default=-1)
    CustomizedItems = models.JSONField(default=list)
    Subtotal = models.DecimalField(max_digits=28, decimal_places=2, default=0)
    Total = models.DecimalField(max_digits=28, decimal_places=2, default=0)

    class Meta:
        db_table = "OrdersInProgress"

    def add_to_order(self, item, selected_items):
        inventory_items = item.DefiniteItems + selected_items
        self.CustomizedItems.append([item.ItemName, str(item.Price), inventory_items])
        self.Subtotal += Decimal(str(item.Price))
        self.Total = (self.Subtotal * Decimal(str(1.0825))).quantize(Decimal('.01'))

    def clear_order(self):
        self.CustomizedItems = []
        self.Subtotal = 0
        self.Total = 0


class RestockOrder(models.Model):
    """
    Model representing a restock order for inventory items.

    Attributes:

    -DateOrdered (DateField): The date the restock order was placed (primary key).
    -DateReceived (DateField): The date the restock order was received (nullable).
    -Items (JSONField): The list of items to be restocked and their quantities.
    -Cost (DecimalField): The total cost of the restock order.
    Meta:

    -db_table (str): The name of the database table to use for storing RestockOrder instances.
    """
    DateOrdered = models.DateField(primary_key=True)
    DateReceived = models.DateField(null=True, blank=True)
    Items = models.JSONField(default=list)
    Cost = models.DecimalField(max_digits=28, decimal_places=2)

    class Meta:
        db_table = "RestockOrders"


class ZReport(models.Model):
    """
    Model representing a Z report, a summary of financial transactions in a cash register at the end of a shift.

    Attributes:
    -DateTimeGenerated (DateTimeField): The date and time the Z report was generated.
    -Subtotal (DecimalField): The subtotal of all transactions in the cash register during the shift.
    -Total (DecimalField): The total amount of money in the cash register at the end of the shift, including tax and any additional fees.

    Meta:
    -db_table (str): The name of the database table to use for this model.
    """

    DateTimeGenerated = models.DateTimeField(primary_key=True)
    Subtotal = models.DecimalField(max_digits=28, decimal_places=2)
    Total = models.DecimalField(max_digits=28, decimal_places=2)

    class Meta:
        db_table = "ZReports"
