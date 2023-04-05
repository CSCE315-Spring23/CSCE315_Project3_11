from pos.models import Order


def generateSalesReport(start_date, end_date):
    orders = Order.objects.filter(DateTimePlaced__range=[start_date, end_date])
    total_value = sum([order.Total for order in orders])
    return total_value
