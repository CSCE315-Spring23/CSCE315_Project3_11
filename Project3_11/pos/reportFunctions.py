from pos.models import Order, ZReport, InventoryItem
from collections import defaultdict
from django.utils import timezone
from django.db.models import Sum
from itertools import combinations

def generateSalesReport(startDate, endDate):
    """
    Generates a sales report for a given date range, including a list of sold menu items, the number of times each
    menu item was sold, and the total value of all orders in the date range.

    Parameters:
    - startDate: a date object representing the start of the date range
    - endDate: a date object representing the end of the date range

    Returns:
    - a tuple containing three elements:
        - a list of sold menu items
        - a list of the number of times each menu item was sold
        - the total value of all orders in the date range
    """
    sales = defaultdict(int)
    orders = Order.objects.filter(DateTimePlaced__gte=startDate, DateTimePlaced__lte=endDate)
    total_value = sum([order.Total for order in orders])
    for order in orders:
        menu_items = order.MenuItemsInOrder
        for item in menu_items:
            sales[item] += 1
    return list(sales), list(sales.values()), total_value

def generateXReport():
    """
    Generates an X report, which is a report of the total sales since the last Z report.

    Returns:
    - the total sales since the last Z report
    """
    # Retrieve the most recent z report
    most_recent_z_report = ZReport.objects.order_by('-DateTimeGenerated').first()

    # Get all orders placed since the most recent z report
    orders_since_z_report = Order.objects.filter(DateTimePlaced__gte=most_recent_z_report.DateTimeGenerated.astimezone(timezone.utc))

    total_sales = orders_since_z_report.aggregate(Sum('Total'))['Total__sum'] or 0

    return total_sales

def generateZReport():
    """
    Generates a Z report, which is a report of the total sales and subtotal since the last Z report. The function
    also inserts a new row into the ZReport table with the calculated values.

    Returns:
    - the total sales since the last Z report
    """
    # Retrieve the most recent z report
    most_recent_z_report = ZReport.objects.order_by('-DateTimeGenerated').first()

    # Get all orders placed since the most recent z report
    orders_since_z_report = Order.objects.filter(DateTimePlaced__gte=most_recent_z_report.DateTimeGenerated.astimezone(timezone.utc))

    # Calculate the total sales and subtotal
    total_sales = orders_since_z_report.aggregate(Sum('Total'))['Total__sum'] or 0
    subtotal = orders_since_z_report.aggregate(Sum('Subtotal'))['Subtotal__sum'] or 0

    # Insert a new row into the ZReport table with the calculated values
    z_report = ZReport.objects.create(
        DateTimeGenerated=timezone.now(),
        Total=total_sales,
        Subtotal=subtotal
    )

    z_report.save()
    print("Z report generated")
    return total_sales

def generateRestockReport(threshold):
    """
    Generates a restock report, which is a list of inventory items that have stock levels below a given threshold.

    Parameters:
    - threshold: an integer representing the minimum stock level required for an item to not be restocked

    Returns:
    - a list of inventory items that have stock levels below the given threshold
    """
    restock_items = []
    for item in InventoryItem.objects.all():
        if item.Stock < threshold:
            restock_items.append(item)
    return restock_items


def generateExcessReport(date):
    """
    Generates an excess report, which is a list of inventory items that have not been sold in sufficient quantities
    since a given date.

    Parameters:
    - date: a datetime object representing the date since which the items' sales will be compared

    Returns:
    - a list of inventory items that have not been sold in sufficient quantities since the given date
    """
    orders = Order.objects.filter(DateTimePlaced__gt=date)

    # Initialize a dictionary to keep track of inventory item servings sold
    servings_sold = defaultdict(int)

    # Parse the orders' item JSONB array and decrement servings sold for each inventory item
    for order in orders:
        items = order.Items
        for item in items:
            servings_sold[item] += 1

    # Get the inventory items that have sold less than their servings
    excess_items = []
    for item in InventoryItem.objects.all():
        if servings_sold[item.Name] < item.Servings:
            excess_items.append(item)

    return excess_items

def whatSalesTogether(time_start, time_end):
    """
    Generates a report of which menu item pairs are sold together most frequently within a given time window.

    Parameters:
    - time_start: a datetime object representing the start of the time window
    - time_end: a datetime object representing the end of the time window

    Returns:
    - a list of tuples, where each tuple contains two menu item names and the number of times they were sold
    together within the time window. The list is sorted in descending order of sales frequency.
    """

    # Query for all orders within the given time window
    pairs = defaultdict(int)
    orders = Order.objects.filter(DateTimePlaced__range=(time_start, time_end))
    for order in orders:
        items = order.MenuItemsInOrder
        for pair in combinations(items, 2):
            pair_str = ','.join(sorted(pair))
            pairs[pair_str] += 1
    sorted_pairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)

    return sorted_pairs
