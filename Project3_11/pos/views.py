import datetime

from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from google.cloud import translate_v2 as translate
from django.conf import settings
from django.shortcuts import redirect

from pos.common_functions import get_sorted_inventory
from pos.models import *
from pos.reportFunctions import *
from pos.inventoryFunctions import *
from pos.menu_functions import *
import datetime as dt
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.models import AccessToken


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
        inventory_items = InventoryItem.objects.all()
        for item in inventory_items:
            print(item.Name)
            print(item.Image)
        for item in menu_items:
            print(item.ItemName)
            print(item.Image)

        # Set other text
        employee_header = 'Employees'
        menu_header = 'Menu'
        inventory_header = 'Inventory'
        employee_table_headers = ['Employee ID', 'Last Name', 'First Name', 'Hire Date', 'PIN', 'Position',
                                  'Hours Worked']
        menu_table_headers = ['Image', 'Item Name', 'Price', 'Definite Items', 'Possible Items']
        inventory_table_headers = ['Image', 'Name', 'Stock', 'NumberNeeded', 'OrderChance', 'Units', 'Category', 'Servings', 'RestockCost']

        # Translate if necessary
        if target_language != 'en':
            # Translate other text
            employee_header = client.translate(employee_header, target_language=target_language)['translatedText']
            menu_header = client.translate(menu_header, target_language=target_language)['translatedText']
            inventory_header = client.translate(inventory_header, target_language=target_language)['translatedText']
            employee_table_headers = [client.translate(header, target_language=target_language)['translatedText'] for
                                      header in employee_table_headers]
            menu_table_headers = [client.translate(header, target_language=target_language)['translatedText'] for header
                                  in menu_table_headers]
            inventory_table_headers = [client.translate(header, target_language=target_language)['translatedText'] for header in inventory_table_headers]

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

            # Translate inventory items
            for inventory_item in inventory_items:
                inventory_item.Name = client.translate(inventory_item.Name, target_language=target_language)['translatedText']
                inventory_item.Units = client.translate(inventory_item.Units, target_language=target_language)['translatedText']
                inventory_item.Category = client.translate(inventory_item.Category, target_language=target_language)['translatedText']

        context = {'employees': employees, 'menu_items': menu_items, 'inventory_items': inventory_items, 'employee_header': employee_header, 'inventory_header': inventory_header,
                   'menu_header': menu_header, 'employee_headers': employee_table_headers, 'inventory_table_headers': inventory_table_headers,
                   'menu_headers': menu_table_headers, 'target_language': target_language}
        return render(request, 'database_info.html', context)


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


def button_testing_page2(request):
    # How to redirect to next page passing name of item to edit
    edit_item = request.POST.get('edit_item', None)
    return render(request, 'button_testing_page2.html', {'edit_item': edit_item})


def order_page(request):
    button_clicked = request.POST.get('button_clicked', None)
    menu = MenuItem.objects.order_by('-Price')
    inventory_items = InventoryItem.objects.all()
    item_categories = {}
    for item in inventory_items:
        if item.Category not in item_categories:
            item_categories[item.Category] = []
        item_categories[item.Category].append(item.Name)
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
                return render(request, 'order_page.html', {'order': OrderInProgress(), 'menu': menu, 'item_categories': item_categories})
        except ValueError:
            order = OrderInProgress()
    else:
        order = OrderInProgress()
    if request.method == 'POST':
        if button_clicked == 'clear_order':
            order.clear_order()
            order.save()
            return HttpResponseRedirect(request.path_info)
        else:
            item_clicked = request.POST.get('menu_item_selected', None)
            if item_clicked:
                item = MenuItem.objects.get(ItemName=item_clicked)
                selected_items = []
                base_selected = request.POST.get('base_selected', None)
                if base_selected:
                    selected_items += [base_selected]
                protein_selected = request.POST.get('protein_selected', None)
                if protein_selected:
                    selected_items += [protein_selected]
                toppings_selected = request.POST.getlist('toppings_selected', None)
                if toppings_selected:
                    selected_items += toppings_selected
                sauce_selected = request.POST.get('sauce_selected', None)
                if sauce_selected:
                    selected_items += [sauce_selected]
                drink_selected = request.POST.get('drink_selected', None)
                if drink_selected:
                    selected_items += [drink_selected]
                if button_clicked == 'add_to_order':
                    order.add_to_order(item, selected_items)
                    order.save()
            request.session['orderpk'] = str(order.DateTimeStarted)
            return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'order_page.html', {'order': order, 'menu': menu, 'item_categories': item_categories})


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


def editInventoryItems(request):
    inventoryItems = InventoryItem.objects.order_by('Category', 'Name')
    return render(request, 'inventoryItems.html', {'inventoryItems':inventoryItems})


def editThisInventoryItem(request):
    editItem = request.POST.get('inventoryItem', None)
    editItem = InventoryItem.objects.get(Name=editItem)
    inventory_items = InventoryItem.objects.order_by('Category')
    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)
    return render(request, 'editThisInventoryItem.html', {'inventoryItem': editItem, 'categories': categories})


def submitInventoryEdit(request):
    if request.method == 'POST':
        editItem = request.POST.get('passedInventoryItem')
        deleteItem = request.POST.get('deleteInventoryItem')
        if deleteItem and not editItem:
            removeInventoryItem(deleteItem)
        editItem = InventoryItem.objects.get(Name=editItem)
        stock = request.POST.get('stock')
        numberNeeded = request.POST.get('numNeeded')
        orderChance = request.POST.get('orderChance')
        units = request.POST.get('units')
        category = request.POST.get('category')
        servings = request.POST.get('servings')
        restockCost = request.POST.get('restockCost')
        image = request.FILES.get('image')
        if stock:
            editItem.Stock = int(stock)
        if numberNeeded:
            editItem.NumberNeeded = int(numberNeeded)
        if orderChance:
            editItem.OrderChance = float(orderChance)
        if units:
            editItem.Units = units
        if category:
            editItem.Category = category
        if servings:
            editItem.Servings = int(servings)
        if restockCost:
            editItem.RestockCost = int(restockCost)
        if image:
            editItem.Image = base64.b64encode(image.read()).decode('utf-8')
        editItem.save()

        inventoryItems = InventoryItem.objects.order_by('Category', 'Name')
        return render(request, 'inventoryItems.html', {'inventoryItems': inventoryItems})
    else:
        inventoryItems = InventoryItem.objects.all()
        return render(request, 'inventoryItems.html', {'inventoryItems': inventoryItems})


def edit_menu_items(request):
    menu_items = MenuItem.objects.order_by('-Price')

    inventory_items = InventoryItem.objects.order_by('Category', 'Name')
    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)

    for item in menu_items:
        item.set_sorted_items("DefiniteItems", inventory_items, categories)
        item.set_sorted_items("PossibleItems", inventory_items, categories)

    return render(request, 'menu_items.html', {'menu_items': menu_items, 'categories': categories})


def edit_this_menu_item(request):
    edit_item = request.POST.get('menu_item', None)
    edit_item = MenuItem.objects.get(ItemName=edit_item)
    inventory_items = InventoryItem.objects.order_by('Category', 'Name')

    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)

    sorted_inventory = get_sorted_inventory(inventory_items, categories)

    edit_item.set_sorted_items("DefiniteItems", inventory_items, categories)
    edit_item.set_sorted_items("PossibleItems", inventory_items, categories)

    return render(request, 'edit_this_menu_item.html', {'menu_item': edit_item, 'inventory_items': inventory_items, 'categories': categories, 'sorted_inventory': sorted_inventory})


def submit_menu_edit(request):
    if request.method == 'POST':
        edit_item = request.POST.get('passed_menu_item', None)
        edit_item = MenuItem.objects.get(ItemName=edit_item)
        image = request.FILES.get('image')
        price = request.POST.get('price')
        definite_items = request.POST.getlist('selected_definite_items')
        possible_items = request.POST.getlist('selected_possible_items')
        if image:
            edit_item.Image = base64.b64encode(image.read()).decode('utf-8')
        if price:
            edit_item.Price = Decimal(price)
        if definite_items:
            edit_item.DefiniteItems = definite_items
        if possible_items:
            edit_item.PossibleItems = possible_items
        edit_item.save()
        return render(request, 'menu_items.html', {'menu_items': MenuItem.objects.order_by('-Price')})
    else:
        return render(request, 'menu_items.html', {'menu_items': MenuItem.objects.order_by('-Price')})


class ValidateUserView(ProtectedResourceView):
        def temp(self):
            print()
#     def dispatch(self, request, *args, **kwargs):
#         try:
#             access_token = AccessToken.objects.get(token=request.GET.get('access_token'))
#         except AccessToken.DoesNotExist:
#             return HttpResponseBadRequest('Invalid access token')
#
#         user = authenticate(request=request, token=access_token)
#         if user is None:
#             return HttpResponseBadRequest('Invalid user')
#
#         login(request, user)
#         return HttpResponse('OK')


def addInventoryItemPage(request):
    inventory_items = InventoryItem.objects.order_by('Category', 'Name')
    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)
    return render(request, 'addInventoryItem.html', {'categories': categories})


def submitInventoryAddition(request):
    if request.method == 'POST':
        # itemToAdd = request.POST.get('passedInventoryItem')
        itemName = request.POST.get('itemName')
        stock = request.POST.get('stock')
        numberNeeded = int(request.POST.get('numNeeded'))
        orderChance = float(request.POST.get('orderChance'))
        units = request.POST.get('units')
        category = request.POST.get('category')
        servings = int(request.POST.get('servings'))
        restockCost = int(request.POST.get('restockCost'))
        image = request.FILES.get('image')
        image = base64.b64encode(image.read()).decode('utf-8')
        addInventoryItem(itemName, stock, numberNeeded, orderChance, units, category, servings, restockCost, image)

        inventoryItems = InventoryItem.objects.order_by('Category', 'Name')
        return render(request, 'inventoryItems.html', {'inventoryItems': inventoryItems})
    else:
        inventoryItems = InventoryItem.objects.all()
        return render(request, 'inventoryItems.html', {'inventoryItems': inventoryItems})

