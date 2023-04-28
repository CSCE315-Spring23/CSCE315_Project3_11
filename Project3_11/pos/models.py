import base64
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from datetime import datetime
from datetime import timedelta
from decimal import Decimal


class Employee(models.Model):
    EmployeeID = models.IntegerField(primary_key=True)
    LastName = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=50)
    HireDate = models.DateField()
    EmployeePIN = models.IntegerField()
    PositionTitle = models.CharField(max_length=50)
    HoursWorked = models.DecimalField(max_digits=28, decimal_places=2)

    class Meta:
        db_table = "Employees"


class ExpirationDate(models.Model):
    UniqueID = models.IntegerField(primary_key=True)
    ItemName = models.TextField()
    ExpirationDate = models.DateTimeField()
    RemainingServings = models.IntegerField()

    class Meta:
        db_table = "ExpirationDates"


class InventoryItem(models.Model):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Image = bytes(self.Image).decode('utf-8')

class MenuItem(models.Model):
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
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_categories()
        self.Image = bytes(self.Image).decode('utf-8')


class Order(models.Model):
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
    DateOrdered = models.DateField(primary_key=True)
    DateReceived = models.DateField(null=True, blank=True)
    Items = models.JSONField(default=list)
    Cost = models.DecimalField(max_digits=28, decimal_places=2)

    class Meta:
        db_table = "RestockOrders"


class ZReport(models.Model):
    DateTimeGenerated = models.DateTimeField(primary_key=True)
    Subtotal = models.DecimalField(max_digits=28, decimal_places=2)
    Total = models.DecimalField(max_digits=28, decimal_places=2)

    class Meta:
        db_table = "ZReports"
