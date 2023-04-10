from pos.models import Order, ZReport, InventoryItem
from collections import defaultdict
from django.utils import timezone
from django.db.models import Sum
from itertools import combinations

def generateSalesReport(startDate, endDate):
    sales = defaultdict(int)
    orders = Order.objects.filter(DateTimePlaced__gte=startDate, DateTimePlaced__lte=endDate)
    total_value = sum([order.Total for order in orders])
    for order in orders:
        menu_items = order.MenuItemsInOrder
        for item in menu_items:
            sales[item] += 1
    return list(sales), list(sales.values()), total_value

def generateXReport():
    # Retrieve the most recent z report
    most_recent_z_report = ZReport.objects.order_by('-DateTimeGenerated').first()

    # Get all orders placed since the most recent z report
    orders_since_z_report = Order.objects.filter(DateTimePlaced__gte=most_recent_z_report.DateTimeGenerated.astimezone(timezone.utc))

    total_sales = orders_since_z_report.aggregate(Sum('Total'))['Total__sum'] or 0

    return total_sales

def generateZReport():
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

def generateRestockReport(threshold):
    restock_items = []
    for item in InventoryItem.objects.all():
        if item.Stock < threshold:
            restock_items.append(item)
    return restock_items


def generateExcessReport(date):
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
