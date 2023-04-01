from django.db import models


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

    class Meta:
        db_table = "InventoryItems"


class MenuItem(models.Model):
    ItemName = models.TextField(primary_key=True)
    Price = models.DecimalField(max_digits=28, decimal_places=2)
    DefiniteItems = models.JSONField(default=list)
    PossibleItems = models.JSONField(default=list)

    class Meta:
        db_table = "MenuItems"


class Order(models.Model):
    DateTimePlaced = models.DateTimeField(primary_key=True)
    EmployeeID = models.IntegerField()
    Items = models.JSONField(default=list)
    Subtotal = models.DecimalField(max_digits=28, decimal_places=2)
    Total = models.DecimalField(max_digits=28, decimal_places=2)
    MenuItemsInOrder = models.JSONField(default=list)

    class Meta:
        db_table = "Orders"


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
