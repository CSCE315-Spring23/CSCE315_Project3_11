from pos.models import InventoryItem


def find_inventory_item(name):
    try:
        item = InventoryItem.objects.get(Name=name)
    except InventoryItem.DoesNotExist:
        return None

    # If an item is found, return a dictionary with its fields
    return {
        "Name": item.Name,
        "Stock": item.Stock,
        "NumberNeeded": item.NumberNeeded,
        "OrderChance": item.OrderChance,
        "Units": item.Units,
        "Category": item.Category,
        "Servings": item.Servings,
        "RestockCost": item.RestockCost
    }
