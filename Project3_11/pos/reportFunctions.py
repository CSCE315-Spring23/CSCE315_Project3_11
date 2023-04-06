from pos.models import Order
from collections import defaultdict

def generateSalesReport(startDate, endDate):
    sales = defaultdict(int)
    orders = Order.objects.filter(DateTimePlaced__gte=startDate, DateTimePlaced__lte=endDate)
    total_value = sum([order.Total for order in orders])
    for order in orders:
        menu_items = order.MenuItemsInOrder
        for item in menu_items:
            sales[item] += 1
    return list(sales), list(sales.values()), total_value

