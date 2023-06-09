import datetime

from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from google.cloud import translate_v2 as translate
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
from bs4 import BeautifulSoup
import requests


def checkPermissions(user_email):
    """
    checks permissions of the users email
    """
    employee_emails = Employee.objects.values_list('Email', flat=True)
    # user_email = request.user.email
    if user_email in employee_emails:
        # employee
        employee = Employee.objects.get(Email=user_email)
        if employee.PositionTitle == "Manager":
            print("Manager")
            return True
        print("Employee")
        return False
    else:
        # customer
        print("Customer")
        return False


def getWeather():
    """
        This function is used when weather data needs to be found for the website.
        It makes a call to the open weather api and returns the kind of weather and temperature.
    """
    APIURLcurrent = r"https://api.openweathermap.org/data/2.5/weather?lat=30.627979&lon=-96.334412&appid=b564f1dbb4cd614c0ee84abe3f4c820c&units=imperial&mode=xml"
    r = requests.get(APIURLcurrent)
    content = BeautifulSoup(r.content, features="xml")

    bigSectionTemp = content.findAll('temperature')
    bigSectionWeather = content.findAll('weather')
    words = 'error'
    temperature = 'error'

    for element in bigSectionWeather:
        words = element.get('value')

    for element in bigSectionTemp:
        temperature = element.get('value')
    return f'{words}, {temperature}'


def login(request):
    """
    Authenticates employee login information by checking if the POST request contains a valid Employee ID and Employee PIN
    in the database. If authentication is successful, it renders the 'employee.html' template with a context containing
    the authenticated employee and weather information retrieved by calling getWeather(). If authentication fails,
    it renders the 'login.html' template with a context containing an error message and weather information retrieved
    by calling getWeather(). If the request method is not POST, it renders the 'login.html' template with weather information
    retrieved by calling getWeather().

    :param request: HTTP request object.
    :return: Rendered HTML template with context containing either authenticated employee and weather information, or an
    error message and weather information, or just weather information.
    """
    if request.method == 'POST':
        employee_id = request.POST['employee_id']
        employee_pin = request.POST['employee_pin']
        try:
            employee = Employee.objects.get(EmployeeID=employee_id, EmployeePIN=employee_pin)
            context = {'employee': employee, 'weather': getWeather()}
            return render(request, 'employee.html', context)
        except Employee.DoesNotExist:
            error = 'Invalid employee ID or PIN'
            context = {'error': error, 'weather': getWeather()}
            return render(request, 'login.html', context)
    return render(request, 'login.html', {'weather': getWeather()})


def employee_page(request):
    """
    Renders the employee page with the given employee ID and PIN. If the HTTP request method is POST, the employee ID and PIN
    are retrieved from the request's POST parameters and used to query the Employee model. If the employee is found, the employee
    page is rendered with the employee object passed as context. Otherwise, a 404 page is returned. If the HTTP request method is
    not POST, the employee page is rendered with a test dictionary passed as context.

    :param request: The HTTP request object.
    :return: A rendered HTML template.
    """
    if request.method == 'POST':
        employee_id = request.POST['EmployeeID']
        employee_pin = request.POST['EmployeePIN']
        employee = get_object_or_404(Employee, EmployeeID=employee_id, EmployeePIN=employee_pin)
        return render(request, 'employee.html', {'employee': employee})
    else:
        content = {'data': 'test hi'}
        return render(request, 'employee.html', content)


def inventory_page(request):
    """
    Renders the inventory page.

    Parameters:
    -----------
    request : HttpRequest
        The request sent to the server.

    Returns:
    --------
    HttpResponse
        The rendered HTML template with the inventory context.
    """
    context = {'inventory': 'test order else'}
    return render(request, 'inventoryItems.html', context)


def reports_page(request):
    """
        Renders the generic reports page when the reports button is clicked on the nav bar.
    """
    print("testing")
    return render(request, 'reports.html')


def order_page(request):
    """
    View function for the order page, where users can create a new order or modify an existing one.

    Parameters:
    - request: the HttpRequest object that contains the GET and POST data sent by the user.

    Returns:
    - HttpResponse object that renders the order page HTML template.

    Behavior:
    - When a GET request is sent, renders the order page template, showing an empty order form.
    - When a POST request is sent, processes the user input data from the order form, and updates the order accordingly.
      - If the "back_button" is clicked, redirects the user to the previous page.
      - If the "clear_order" button is clicked, clears the current order and redirects the user to the order page.
      - If a menu item is selected and the "add_to_order" button is clicked, adds the selected menu item to the order.
      - If the "place_order" button is clicked, finalizes the order, creates a new Order object, and saves it to the database.
    - The rendered HTML template displays the current order items, menu items, and inventory items, as well as options for the user to modify the current order or place the final order.

    """
    button_clicked = request.POST.get('button_clicked', None)
    if button_clicked == 'back_button':
        return HttpResponseRedirect(request.path_info)
    menu = MenuItem.objects.order_by('-Price')
    permissions = checkPermissions(request.user.email)
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
                finished_order = Order(EmployeeID=order.EmployeeID, Items=items, Subtotal=order.Subtotal,
                                       Total=order.Total, MenuItemsInOrder=menu_items_in_order)
                finished_order.save()
                order.delete()
                del request.session['orderpk']
                return render(request, 'order_page.html',
                              {'order': OrderInProgress(), 'menu': menu, 'item_categories': item_categories,
                               'permissions': permissions})
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
        return render(request, 'order_page.html',
                      {'order': order, 'menu': menu, 'item_categories': item_categories, 'weather': getWeather(),
                       'permissions': permissions})


def salesReport(request):
    """
        Renders the base of the sales report page that takes inputs to be ready to generate reports
    """
    return render(request, 'salesReport.html')


def xReport(request):
    """
        Renders the base of the x report page has a button to generate reports
    """
    return render(request, 'xReport.html')


def zReport(request):
    """
        Renders the base of the x report page has a button to generate reports
    """
    return render(request, 'zReport.html')


def excessReport(request):
    """
        Renders the base of the excess report page that takes inputs to be ready to generate reports
    """
    return render(request, 'excessReport.html')


def restockReport(request):
    """
        Renders the base of the restock report page that takes inputs to be ready to generate reports
    """
    return render(request, 'restockReport.html')


def whatSalesTogetherReport(request):
    """
        Renders the base of the what sales together report page that takes inputs to be ready to generate reports
    """
    return render(request, 'whatSalesTogetherReport.html')


def salesReportGeneration(request):
    """
        Generates the appropriate data from the backend functions with the user's inputs to display on the reports page
    """
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
    """
        Generates the appropriate data from the backend functions to display on the reports page
    """
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
    """
        Generates the appropriate data from the backend functions to display on the reports page
    """
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
    """
        Generates the appropriate data from the backend functions with the user's inputs to display on the reports page
    """
    if request.method == 'POST':
        datePlaced = request.POST['datePlaced']
        try:
            excess_items = generateExcessReport(
                timezone.make_aware(dt.datetime.strptime(datePlaced, '%Y-%m-%dT%H:%M'),
                                    timezone.get_current_timezone()))
        except ValueError:
            context = {'excessReportData': ['Please input a valid datetime']}
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
    """
        Generates the appropriate data from the backend functions with the user's inputs to display on the reports page
    """
    if request.method == 'POST':
        threshold = int(request.POST['threshold'])
        if threshold > 0:
            restock_items = generateRestockReport(threshold)
        else:
            context = {'restockReportData': ['Please input a valid number']}
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
    """
        Generates the appropriate data from the backend functions with the user's inputs to display on the reports page
    """
    if request.method == 'POST':
        startDate = request.POST['startDate']
        endDate = request.POST['endDate']
        try:
            sorted_pairs = whatSalesTogether(
                timezone.make_aware(dt.datetime.strptime(startDate, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone()),
                timezone.make_aware(dt.datetime.strptime(endDate, '%Y-%m-%dT%H:%M'), timezone.get_current_timezone()))
        except ValueError:
            context = {'whatSalesTogetherReportData': [['Please input a valid datetime', '']]}
            return render(request, 'whatSalesTogetherReport.html', context)

        context = {'whatSalesTogetherReportData': sorted_pairs[0:5]}
        return render(request, 'whatSalesTogetherReport.html', context)
    else:
        return render(request, 'whatSalesTogetherReport.html')


def editInventoryItems(request):
    """
        Generates the categories for the adding inventory item form and displays the form
    """
    inventoryItems = InventoryItem.objects.order_by('Category', 'Name')
    return render(request, 'inventoryItems.html', {'inventoryItems': inventoryItems})


def editThisInventoryItem(request):
    """
    Display a form to edit a specific inventory item.

    The view expects a POST request containing the name of the inventory item
    to be edited in the 'inventoryItem' parameter. The view retrieves the item
    from the database and renders the 'editThisInventoryItem.html' template,
    which displays a form with the current values of the item's attributes.

    The form allows the user to edit the item's category, name, quantity, unit,
    and notes. The category and unit fields are populated with all existing
    categories and units, respectively. The user can also delete the item.

    After submitting the form via a POST request, the view saves the edited
    item to the database and redirects to the 'inventoryItems' page.

    Parameters:
    -----------
    request : HttpRequest
        The request object containing the HTTP request data.

    Returns:
    --------
    HttpResponse
        The HTTP response object containing the rendered template with the
        inventory item form.
    """
    editItem = request.POST.get('inventoryItem', None)
    editItem = InventoryItem.objects.get(Name=editItem)
    inventory_items = InventoryItem.objects.order_by('Category')
    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)
    return render(request, 'editThisInventoryItem.html', {'inventoryItem': editItem, 'categories': categories})


def submitInventoryEdit(request):
    """
        Processes the form's data and edits the inventory item based on it
    """
    if request.method == 'POST':
        editItem = request.POST.get('passedInventoryItem', None)
        deleteItem = request.POST.get('deleteInventoryItem', None)
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
    """
    Renders the "edit_menu_items.html" template to display a list of all the menu items in the database, sorted by price, as well as a list of all the categories for inventory items.

    Context:
    - menu_items: a QuerySet of all the MenuItem objects in the database, ordered by descending price.
    - categories: a list of all the categories for InventoryItem objects in the database, in alphabetical order.

    Template:
    - "edit_menu_items.html"
    """
    menu_items = MenuItem.objects.order_by('-Price')

    inventory_items = InventoryItem.objects.order_by('Category', 'Name')
    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)

    return render(request, 'edit_menu_items.html', {'menu_items': menu_items, 'categories': categories})


def edit_this_menu_item(request):
    """
    Display the page to edit a specific menu item and process the form submission to save the changes.

    If the request method is POST, update the selected menu item with the new information and save the changes.
    Otherwise, display the page with the information of the selected menu item.

    Parameters:
    - request: HttpRequest object containing information about the current request

    Returns:
    - HttpResponse object with the rendered HTML page displaying the selected menu item's information
    """
    edit_item = request.POST.get('menu_item', None)
    edit_item = MenuItem.objects.get(ItemName=edit_item)
    inventory_items = InventoryItem.objects.order_by('Category', 'Name')

    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)

    sorted_inventory = get_sorted_inventory(inventory_items, categories)

    return render(request, 'edit_this_menu_item.html',
                  {'menu_item': edit_item, 'inventory_items': inventory_items, 'categories': categories,
                   'sorted_inventory': sorted_inventory})


def submit_menu_edit(request):
    """
    View that allows for editing of a menu item.

    The view retrieves the menu item to be edited from the POST request, as well as any updates to the menu item's
    image, price, and possible/definite ingredient items. If the delete button was clicked instead, the corresponding
    menu item is deleted.

    Parameters:
    request(HttpRequest): The HTTP request object sent by the client

    Returns:
    HttpResponse: The HTTP response object that contains either the updated edit menu items page or the original
    edit menu items page with the current menu items.

    """
    if request.method == 'POST':
        edit_item = request.POST.get('passed_menu_item', None)
        delete_item = request.POST.get('delete_menu_item', None)
        if delete_item and not edit_item:
            removeMenuItem(delete_item)
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
        return render(request, 'edit_menu_items.html', {'menu_items': MenuItem.objects.order_by('-Price')})
    else:
        return render(request, 'edit_menu_items.html', {'menu_items': MenuItem.objects.order_by('-Price')})


def add_menu_item(request):
    """
    Render a template for adding a new menu item, including all inventory items and categories, sorted for display.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        A rendered HTML template for adding a new menu item, including all inventory items and categories, sorted for display.
    """
    menu_items = MenuItem.objects.order_by('-Price')
    inventory_items = InventoryItem.objects.order_by('Category', 'Name')

    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)

    sorted_inventory = get_sorted_inventory(inventory_items, categories)

    return render(request, 'add_menu_item.html', {'menu_items': menu_items, 'inventory_items': inventory_items, 'categories': categories, 'sorted_inventory': sorted_inventory})


def submit_menu_item_addition(request):
    """
    Handle a POST request to add a new menu item to the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        A rendered HTML template for editing menu items in the database.
    """
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        definite_items = request.POST.getlist('selected_definite_items')
        possible_items = request.POST.getlist('selected_possible_items')
        image = request.FILES.get('image')
        image = base64.b64encode(image.read()).decode('utf-8')
        add_to_menu(item_name, price, definite_items, possible_items, bytes(image, 'utf-8'))
        return render(request, 'edit_menu_items.html', {'menu_items': MenuItem.objects.order_by('-Price')})
    else:
        return render(request, 'edit_menu_items.html', {'menu_items': MenuItem.objects.order_by('-Price')})


class ValidateUserView(ProtectedResourceView):
    """
    used for validating user login
    """
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
    """
        Generates the categories for the adding inventory item form and displays the form
    """
    inventory_items = InventoryItem.objects.order_by('Category', 'Name')
    categories = []
    for item in inventory_items:
        if item.Category not in categories:
            categories.append(item.Category)
    return render(request, 'addInventoryItem.html', {'categories': categories})


def submitInventoryAddition(request):
    """
        Processes the form's data and creates a new inventory item based on it
    """
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


def menuBoard(request):
    """
        Generates a menu and displays the menu board
    """
    menu = MenuItem.objects.order_by('-Price')
    return render(request, 'menuBoard.html',
                  {'menu': menu, 'weather': getWeather()})
