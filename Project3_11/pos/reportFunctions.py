from pos.models import Order, ZReport
from collections import defaultdict
from django.utils import timezone
from django.db.models import Sum

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
