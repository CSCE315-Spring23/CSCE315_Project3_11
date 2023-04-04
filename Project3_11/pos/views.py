from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from pos.models import *


def login(request):
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        employee_pin = request.POST['employee_pin']
        try:
            employee = Employee.objects.get(EmployeeID=employee_id, EmployeePIN=employee_pin)
            context = {'employee': employee}
            return render(request, 'employee.html', context)
        except Employee.DoesNotExist:
            error = 'Invalid employee ID or PIN'
            context = {'error': error}
            return render(request, 'login.html', context)
    return render(request, 'login.html')


def employee_page(request):
    if request.method == 'POST':
        employee_id = request.POST['EmployeeID']
        employee_pin = request.POST['EmployeePIN']
        employee = get_object_or_404(Employee, EmployeeID=employee_id, EmployeePIN=employee_pin)
        return render(request, 'employee.html', {'employee': employee})
    else:
        content = {'data': 'test hi'}
        return render(request, 'employee.html', content)


def menuItems(request):
    fullMenu = MenuItem.objects.all().values()
    print(fullMenu)
    content = {'menuTest': fullMenu}
    return HttpResponse(render(request, 'employee.html', content))


def database_info(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        expiration_dates = ExpirationDate.objects.all()
        inventory_items = InventoryItem.objects.all()
        menu_items = MenuItem.objects.all()
        orders = Order.objects.all()
        restock_orders = RestockOrder.objects.all()
        z_reports = ZReport.objects.all()
        context = {'employees': employees, 'expiration_dates': expiration_dates, 'inventory_items': inventory_items,
                   'menu_items': menu_items, 'orders': orders, 'restock_orders': restock_orders, 'z_reports': z_reports}
        return render(request, 'database_info.html', context)
