from pos.models import InventoryItem


def findInventoryItem(name):
    """
    Returns a dictionary containing information about an inventory item with the given name.

    Parameters:
        name (str): The name of the inventory item to search for.

    Returns:
        dict: A dictionary containing information about the inventory item with the given name. If no such item is found, returns None.
    """
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
    """
    Adds a new inventory item to the database with the given attributes.

    Parameters:
        name (str): The name of the new inventory item. Defaults to "null".
        stock (int): The current stock of the new inventory item. Defaults to -1.
        number_needed (int): The minimum number of the new inventory item that should be kept in stock. Defaults to -1.
        order_chance (float): The chance that an order will be placed for the new inventory item. Defaults to -1.0.
        units (str): The units in which the new inventory item is measured. Defaults to "null".
        category (str): The category to which the new inventory item belongs. Defaults to "null".
        servings (int): The number of servings that can be made from the new inventory item. Defaults to -1.
        restock_cost (float): The cost of restocking the new inventory item. Defaults to -1.
    """
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
    """
    Removes an inventory item from the database with the given name.

    Parameters:
        name (str): The name of the inventory item to remove.
    """
    try:
        item = InventoryItem.objects.get(Name=name)
        item.delete()
    except InventoryItem.DoesNotExist:
        print(f"Inventory item '{name}' not found in database.")
