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
