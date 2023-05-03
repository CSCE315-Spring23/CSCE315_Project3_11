def get_category(item_name, inventory):
    """
    Returns the category of the given item name from the inventory list.

    Args:
        item_name (str): The name of the item to retrieve the category for.
        inventory (list): A list of inventory items.

    Returns:
        str: The category of the item.
    """
    for item in inventory:
        if item.Name == item_name:
            return item.Category


def count_items_by_category(inventory_items, categories):
    """
    Counts the number of inventory items by category.

    Args:
        inventory_items (list): A list of inventory items.
        categories (list): A list of categories to count items for.

    Returns:
        dict: A dictionary where the keys are the categories and the values are the counts of items for that category.
    """
    count_dict = {category: 0 for category in categories}
    for item in inventory_items:
        for category in categories:
            if get_category(item.Name, inventory_items) == category:
                count_dict[category] += 1
    return count_dict


def get_sorted_inventory(inventory_items, categories):
    """
    Returns a sorted inventory list by category.

    Args:
        inventory_items (list): A list of inventory items.
        categories (list): A list of categories to sort the items by.

    Returns:
        list: A 2D list where each row represents a category and each column represents an inventory item for that category.
    """
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
