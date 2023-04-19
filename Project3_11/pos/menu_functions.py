from pos.models import MenuItem


def add_to_menu(item_name, price, definite_items, possible_items):
    new_item = MenuItem(ItemName=item_name, Price=price, DefiniteItems=definite_items, PossibleItems=possible_items)
    new_item.save()

def removeMenuItem(name):
    try:
        item = MenuItem.objects.get(Name=name)
        item.delete()
    except MenuItem.DoesNotExist:
        print(f"Inventory item '{name}' not found in database.")