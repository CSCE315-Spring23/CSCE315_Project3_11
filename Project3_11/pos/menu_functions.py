from pos.models import MenuItem, InventoryItem


def add_to_menu(item_name, price, definite_items, possible_items):
    """
    Adds a new item to the menu.

    Args:
        item_name (str): The name of the item to be added.
        price (float): The price of the item.
        definite_items (list): A list of definite items that must be included in the item.
        possible_items (list): A list of possible items that can be included in the item.

    Returns:
        None
    """
    new_item = MenuItem(ItemName=item_name, Price=price, DefiniteItems=definite_items, PossibleItems=possible_items)
    new_item.save()

def removeMenuItem(name):
    """
    Removes an item from the menu.

    Args:
        name (str): The name of the item to be removed.

    Returns:
        None
    """
    try:
        item = MenuItem.objects.get(Name=name)
        item.delete()
    except MenuItem.DoesNotExist:
        print(f"Inventory item '{name}' not found in database.")

