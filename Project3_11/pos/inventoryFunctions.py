from pos.models import InventoryItem


def findInventoryItem(name):
    try:
        item = InventoryItem.objects.get(Name=name)
        return {
            "Name": item.Name,
            "Stock": item.Stock,
            "NumberNeeded": item.NumberNeeded,
            "OrderChance": item.OrderChance,
            "Units": item.Units,
            "Category": item.Category,
            "Servings": item.Servings,
            "RestockCost": item.RestockCost,
        }
    except InventoryItem.DoesNotExist:
        return None

def addInventoryItem(name="null", stock=-1, number_needed=-1, order_chance=-1.0, units="null", category="null", servings=-1, restock_cost=-1):
    # create a new inventory item object with the given attributes
    new_item = InventoryItem(
        Name=name,
        Stock=stock,
        NumberNeeded=number_needed,
        OrderChance=order_chance,
        Units=units,
        Category=category,
        Servings=servings,
        RestockCost=restock_cost
    )
    # save the new item to the database
    new_item.save()

def removeInventoryItem(name):
    try:
        item = InventoryItem.objects.get(Name=name)
        item.delete()
    except InventoryItem.DoesNotExist:
        print(f"Inventory item '{name}' not found in database.")


def get_category(item_name, inventory):
    for item in inventory:
        if item.Name == item_name:
            return item.Category
