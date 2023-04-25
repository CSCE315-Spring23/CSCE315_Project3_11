import datetime

from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from google.cloud import translate_v2 as translate
from django.conf import settings
from django.shortcuts import redirect
from pos.models import *
from pos.reportFunctions import *
import datetime as dt
from django.http import HttpResponseRedirect


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
    return render(request, 'inventoryItems.html', context)


def reports_page(request):
    print("testing")
    return render(request, 'reports.html')


def menuItems(request):
    fullMenu = MenuItem.objects.all().values()
    print(fullMenu)
    content = {'menuTest': fullMenu}
    return HttpResponse(render(request, 'menuItems.html', content))


def database_info(request):
    if request.method == 'GET':
        client = translate.Client(credentials=settings.CREDENTIALS)
        target_language = request.session.get(settings.LANGUAGE_SESSION_KEY, 'en')

        # Get database information
        employees = Employee.objects.all()
        menu_items = MenuItem.objects.all()

        # Set other text
        employee_header = 'Employees'
        menu_header = 'Menu'
        employee_table_headers = ['Employee ID', 'Last Name', 'First Name', 'Hire Date', 'PIN', 'Position',
                                  'Hours Worked']
        menu_table_headers = ['Item Name', 'Price', 'Definite Items', 'Possible Items']

        # Translate if necessary
        if target_language != 'en':
            # Translate other text
            employee_header = client.translate(employee_header, target_language=target_language)['translatedText']
            menu_header = client.translate(menu_header, target_language=target_language)['translatedText']
            employee_table_headers = [client.translate(header, target_language=target_language)['translatedText'] for
                                      header in employee_table_headers]
            menu_table_headers = [client.translate(header, target_language=target_language)['translatedText'] for header
                                  in menu_table_headers]

            # Translate employees
            for employee in employees:
                employee.PositionTitle = client.translate(employee.PositionTitle, target_language=target_language)[
                    'translatedText']

            # Translate menu items
            for menu_item in menu_items:
                menu_item.ItemName = client.translate(menu_item.ItemName, target_language=target_language)[
                    'translatedText']
                translated_definite_items = []
                for definite_item in menu_item.DefiniteItems:
                    translated_definite_items += [
                        client.translate(definite_item, target_language=target_language)['translatedText']]
                menu_item.DefiniteItems = translated_definite_items
                translated_possible_items = []
                for possible_item in menu_item.PossibleItems:
                    translated_possible_items += [
                        client.translate(possible_item, target_language=target_language)['translatedText']]
                menu_item.PossibleItems = translated_possible_items

        context = {'employees': employees, 'menu_items': menu_items, 'employee_header': employee_header,
                   'menu_header': menu_header, 'employee_headers': employee_table_headers,
                   'menu_headers': menu_table_headers, 'target_language': target_language}
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


def set_language(request):
    language = request.POST.get('language')

    # Store the language in the session
    request.session[settings.LANGUAGE_SESSION_KEY] = language

    if language:
        request.session['django_language'] = language
    return redirect(request.META.get('HTTP_REFERER', '/'))


def button_testing(request):
    order_total = request.session.get('order_total', 0)
    menu = MenuItem.objects.all()
    if request.method == 'POST':
        button_clicked = request.POST.get('button_clicked', None)
        if button_clicked == 'reset':
            order_total = '0'
        else:
            item_clicked = request.POST.get('item_clicked', None)
            if item_clicked:
                item = MenuItem.objects.get(ItemName=item_clicked)
                order_total = str(Decimal(order_total) + item.Price)
        request.session['order_total'] = order_total
    return render(request, 'button_testing.html', {'order_total': order_total, 'menu': menu})


def order_page(request):
    button_clicked = request.POST.get('button_clicked', None)
    menu = MenuItem.objects.all()
    if 'orderpk' in request.session:
        str_time = request.session['orderpk']
        try:
            order = OrderInProgress.objects.get(DateTimeStarted=datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S.%f'))
            if button_clicked == 'place_order':
                items = []
                menu_items_in_order = []
                for customized_item in order.CustomizedItems:
                    items += [customized_item[0]]
                    menu_items_in_order += customized_item[2]
                finished_order = Order(EmployeeID=order.EmployeeID, Items=items, Subtotal=order.Subtotal, Total=order.Total, MenuItemsInOrder=menu_items_in_order)
                finished_order.save()
                order.delete()
                del request.session['orderpk']
                return render(request, 'order_page.html', {'order': OrderInProgress(), 'menu': menu})
        except ValueError:
            order = OrderInProgress()
    else:
        order = OrderInProgress()
    if request.method == 'POST':
        if button_clicked == 'reset':
            order.clear_order()
            order.save()
            return HttpResponseRedirect(request.path_info)  # redirect to same page to avoid form resubmission
        else:
            item_clicked = request.POST.get('item_clicked', None)
            if item_clicked:
                item = MenuItem.objects.get(ItemName=item_clicked)
                selected_items = []
                toppings_clicked = request.POST.getlist('topping_clicked', None)
                if toppings_clicked:
                    selected_items = toppings_clicked
                order.add_to_order(item, selected_items)
                order.save()
            request.session['orderpk'] = str(order.DateTimeStarted)
            return HttpResponseRedirect(request.path_info)  # redirect to same page to avoid form resubmission
    else:
        return render(request, 'order_page.html', {'order': order, 'menu': menu})


def salesReport(request):
    return render(request, 'salesReport.html')


def xReport(request):
    return render(request, 'xReport.html')


def zReport(request):
    return render(request, 'zReport.html')


def excessReport(request):
    return render(request, 'excessReport.html')


def restockReport(request):
    return render(request, 'restockReport.html')


def whatSalesTogetherReport(request):
    return render(request, 'whatSalesTogetherReport.html')


def salesReportGeneration(request):
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        try:
            sales, salesValues, total_value = generateSalesReport(
                timezone.make_aware(dt.datetime.strptime(startDate, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone()),
                timezone.make_aware(dt.datetime.strptime(endDate, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone()))
        except ValueError:
            context = {'salesReportData': 'Please input a valid datetime'}
            return render(request, 'salesReport.html', context)
        # sales will be the list of menu items ordered
        print(sales)
        # salesValues will be the amount of times each menu item was ordered
        print(salesValues)
        # total_value will be the sum of all the sales in the time period
        print(total_value)
        context = {'salesReportData': total_value}
        return render(request, 'salesReport.html', context)
    else:
        return render(request, 'salesReport.html')


def xReportGeneration(request):
    if request.method == 'POST':
        try:
            total_sales = generateXReport()
        except ValueError:
            context = {'xReportData': 'Please input a valid datetime'}
            return render(request, 'xReport.html', context)
        # total_value will be the sum of all the sales in the time period
        print(total_sales)
        context = {'xReportData': total_sales}
        return render(request, 'xReport.html', context)
    else:
        return render(request, 'xReport.html')


def zReportGeneration(request):
    if request.method == 'POST':
        try:
            total_sales = generateZReport()
        except ValueError:
            context = {'zReportData': 'Please input a valid datetime'}
            return render(request, 'zReport.html', context)
        # total_value will be the sum of all the sales in the time period
        print(total_sales)
        context = {'zReportData': total_sales}
        return render(request, 'zReport.html', context)
    else:
        return render(request, 'zReport.html')


def excessReportGeneration(request):
    if request.method == 'POST':
        datePlaced = request.POST['datePlaced']
        try:
            excess_items = generateExcessReport(
                timezone.make_aware(dt.datetime.strptime(datePlaced, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone()))
        except ValueError:
            context = {'excessReportData': 'Please input a valid datetime'}
            return render(request, 'excessReport.html', context)
        # total_value will be the sum of all the sales in the time period
        print(excess_items)
        excessItemNames = []
        for item in excess_items:
            excessItemNames.append(item.Name)
        context = {'excessReportData': excessItemNames}
        return render(request, 'excessReport.html', context)
    else:
        return render(request, 'excessReport.html')


def restockReportGeneration(request):
    if request.method == 'POST':
        threshold = int(request.POST['threshold'])
        if threshold > 0:
            restock_items = generateRestockReport(threshold)
        else:
            context = {'restockReportData': 'Please input a valid number'}
            return render(request, 'restockReport.html', context)
        # total_value will be the sum of all the sales in the time period
        print(restock_items)
        restockItemNames = []
        for item in restock_items:
            restockItemNames.append(item.Name)
        context = {'restockReportData': restockItemNames}
        return render(request, 'restockReport.html', context)
    else:
        return render(request, 'restockReport.html')


def whatSalesTogetherReportGeneration(request):
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        try:
            sorted_pairs = whatSalesTogether(
                timezone.make_aware(dt.datetime.strptime(startDate, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone()),
                timezone.make_aware(dt.datetime.strptime(endDate, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone()))
        except ValueError:
            context = {'whatSalesTogetherReportData': 'Please input a valid datetime'}
            return render(request, 'whatSalesTogetherReport.html', context)
        # sales will be the list of menu items ordered
        print(sorted_pairs)

        context = {'whatSalesTogetherReportData': sorted_pairs}
        return render(request, 'whatSalesTogetherReport.html', context)
    else:
        return render(request, 'whatSalesTogetherReport.html')
