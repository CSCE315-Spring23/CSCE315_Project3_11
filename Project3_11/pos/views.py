from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from google.cloud import translate_v2 as translate

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

def order_page(request):
        context = {'order': 'test order else'}
        return render(request, 'order.html', context)


def inventory_page(request):
    context = {'inventory': 'test order else'}
    return render(request, 'inventoryItems.html ', context)

def reports_page(request):
    context = {'reports': 'test order else'}
    return render(request, 'reports.html', context)



def menuItems(request):
    fullMenu = MenuItem.objects.all().values()
    print(fullMenu)
    content = {'menuTest': fullMenu}
    return HttpResponse(render(request, 'menuItems.html', content))


def database_info(request):
    if request.method == 'GET':
        client = translate.Client()
        target_language = 'es'

        # Get database information
        employees = Employee.objects.all()
        menu_items = MenuItem.objects.all()

        # Set other text
        employee_header = 'Employees'
        menu_header = 'Menu'
        employee_table_headers = ['Employee ID', 'Last Name', 'First Name', 'Hire Date', 'PIN', 'Position', 'Hours Worked']
        menu_table_headers = ['Item Name', 'Price', 'Definite Items', 'Possible Items']

        # Translate if necessary
        if target_language != 'en':
            # Translate other text
            employee_header = client.translate(employee_header, target_language=target_language)['translatedText']
            menu_header = client.translate(menu_header, target_language=target_language)['translatedText']
            employee_table_headers = [client.translate(header, target_language=target_language)['translatedText'] for header in employee_table_headers]
            menu_table_headers = [client.translate(header, target_language=target_language)['translatedText'] for header in menu_table_headers]

            # Translate employees
            for employee in employees:
                employee.PositionTitle = client.translate(employee.PositionTitle, target_language=target_language)['translatedText']

            # Translate menu items
            for menu_item in menu_items:
                menu_item.ItemName = client.translate(menu_item.ItemName, target_language=target_language)['translatedText']
                translated_definite_items = []
                for definite_item in menu_item.DefiniteItems:
                    translated_definite_items += [client.translate(definite_item, target_language=target_language)['translatedText']]
                menu_item.DefiniteItems = translated_definite_items
                translated_possible_items = []
                for possible_item in menu_item.PossibleItems:
                    translated_possible_items += [client.translate(possible_item, target_language=target_language)['translatedText']]
                menu_item.PossibleItems = translated_possible_items

        context = {'employees': employees, 'menu_items': menu_items,'employee_header': employee_header, 'menu_header': menu_header, 'employee_headers': employee_table_headers, 'menu_headers': menu_table_headers}
        return render(request, 'database_info.html', context)


def addItemToOrder(request):
    # if request.method == 'POST':
    #     button_name = request.POST.get('buttonTesting', '')
    #     # Logic to add text to the website based on the button name
    #     text = ":P {}".format(button_name)
    #     context = {'text': text}
    #     return render(request, 'menuItems.html', context)
    # else:
    #     # Handle GET request
    #     return render(request, 'menuItems.html')
    # content = {'items': 'test hi'}
    # return render(request, 'menuItems.html', content)
    return HttpResponse(render(request, 'menuItems.html'))


def submitOrder(request):
    return HttpResponse(render(request, 'menuItems.html'))
