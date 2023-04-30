from pos.inventoryFunctions import get_category
from pos.models import MenuItem, InventoryItem


def add_to_menu(item_name, price, definite_items, possible_items):
    new_item = MenuItem(ItemName=item_name, Price=price, DefiniteItems=definite_items, PossibleItems=possible_items)
    new_item.save()

def removeMenuItem(name):
    try:
        item = MenuItem.objects.get(Name=name)
        item.delete()
    except MenuItem.DoesNotExist:
        print(f"Inventory item '{name}' not found in database.")


def count_items_by_category(menu_item, categories, list_name):
    inventory = InventoryItem.objects.all()
    count_dict = {category: 0 for category in categories}
    if list_name == "DefiniteItems":
        for item in menu_item.DefiniteItems:
            for category in categories:
                if get_category(item, inventory) == category:
                    count_dict[category] += 1
    elif list_name == "PossibleItems":
        for item in menu_item.PossibleItems:
            for category in categories:
                if get_category(item, inventory) == category:
                    count_dict[category] += 1
    return count_dict


def get_sorted_items(menu_item, inventory, categories, list_name):
    count_dict = count_items_by_category(menu_item, categories, list_name)
    columns = len(categories)
    rows = max(count_dict.values())
    sorted_items = [["" for i in range(columns)] for j in range(rows)]
    items_list = []
    if list_name == "DefiniteItems":
        items_list = menu_item.DefiniteItems
    elif list_name == "PossibleItems":
        items_list = menu_item.PossibleItems

    for item_name in items_list:
        i = 0
        for category in categories:
            if get_category(item_name, inventory) == category:
                for j in range(rows):
                    if sorted_items[j][i] == "":
                        sorted_items[j][i] = item_name
                        break
            i += 1
    return sorted_items
