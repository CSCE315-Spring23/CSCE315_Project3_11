def get_category(item_name, inventory):
    for item in inventory:
        if item.Name == item_name:
            return item.Category


def count_items_by_category(inventory_items, categories):
    count_dict = {category: 0 for category in categories}
    for item in inventory_items:
        for category in categories:
            if get_category(item.Name, inventory_items) == category:
                count_dict[category] += 1
    return count_dict


def get_sorted_inventory(inventory_items, categories):
    count_dict = count_items_by_category(inventory_items, categories)
    columns = len(categories)
    rows = max(count_dict.values())
    sorted_items = [["" for i in range(columns)] for j in range(rows)]

    for item in inventory_items:
        i = 0
        for category in categories:
            if get_category(item.Name, inventory_items) == category:
                for j in range(rows):
                    if sorted_items[j][i] == "":
                        sorted_items[j][i] = item.Name
                        break
            i += 1

    return sorted_items
