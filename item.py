"""Item catalogue, inventory, and shop functions."""
import os
from config import BASE_DIR, ITEMS_FILE, MAX_INVENTORY_WEIGHT
from errors import InventoryFullError, NotEnoughGoldError
def _parse_item_line(parts, line_number):
    """Validate one item row and return its normalized record."""
    if len(parts) != 6:
        print(f"Warning: invalid row {line_number} in items.txt; skipping it.")
        return None
    item_id, name, item_type = parts[:3]
    try:
        power, price, weight = map(int, parts[3:])
    except ValueError:
        print(f"Warning: invalid number in items.txt row {line_number}.")
        return None
    item_type = item_type.lower()
    if not item_id or not name or item_type not in ("heal", "weapon", "armor"):
        print(f"Warning: invalid item data in row {line_number}.")
        return None
    if min(power, price, weight) < 0 or weight == 0:
        print(f"Warning: invalid values in items.txt row {line_number}.")
        return None
    return item_id.lower(), {
        "name": name, "type": item_type, "power": power,
        "price": price, "weight": weight,
    }
def load_items(filename=None):
    """Load item records; skip malformed rows without losing valid records."""
    filename = filename or os.path.join(BASE_DIR, "items.txt")
    items = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                record = _parse_item_line([part.strip() for part in line.split("|")], line_number)
                if record is None:
                    continue
                item_id, item = record
                if item_id in items:
                    print(f"Warning: duplicate item ID {item_id} in items.txt; skipping it.")
                    continue
                items[item_id] = item
    except FileNotFoundError:
        print("Warning: items.txt was not found; the item catalog is empty.")
        try:
            open(filename, "a", encoding="utf-8").close()
        except OSError:
            pass
    return items
def show_shop(items):
    """Print all item definitions loaded from items.txt."""
    print("\n===== Shop =====")
    if not items:
        print("No items are defined in items.txt.")
        return
    for item_id, item in items.items():
        print(f"{item_id} - {item['name']} | Type: {item['type']} | Effect: {item['power']} | Price: {item['price']} | Weight: {item['weight']}")
def show_inventory(hero, items):
    """Print carried items, equipment status, total weight, and gold."""
    print("\n===== Inventory =====")
    if not hero.inventory:
        print("Your inventory is empty.")
    for item_id, quantity in hero.inventory.items():
        item = items.get(item_id)
        if item is None:
            print(f"{item_id} | Quantity: {quantity} | Warning: not defined in items.txt")
            continue
        marker = " (equipped)" if item_id in hero.equipped else ""
        print(f"{item['name']} | Quantity: {quantity} | Weight each: {item['weight']}{marker}")
    print(f"Total weight: {hero.inventory_weight(items)} / {MAX_INVENTORY_WEIGHT}")
    print("Gold:", hero.gold)
def find_item_key(name, items):
    """Find an item by ID or display name, ignoring letter case."""
    name = name.strip().casefold()
    for item_id, item in items.items():
        if name in (item_id.casefold(), item["name"].casefold()):
            return item_id
    return None
def add_item(hero, item_id):
    """Add one item unit to the hero inventory."""
    hero.inventory[item_id] = hero.inventory.get(item_id, 0) + 1
def buy_item(hero, items, logger=None):
    """Buy one item if the hero has enough gold and carrying capacity."""
    show_shop(items)
    item_key = find_item_key(input("Item name or ID to buy: "), items)
    if item_key is None:
        print("Item not found.")
        return False
    item = items[item_key]
    if hero.gold < item["price"]:
        raise NotEnoughGoldError("You do not have enough gold.")
    if hero.inventory_weight(items) + item["weight"] > MAX_INVENTORY_WEIGHT:
        raise InventoryFullError("Your inventory is full. Drop an item first.")
    hero.gold -= item["price"]
    add_item(hero, item_key)
    print("Purchased:", item["name"])
    if logger:
        logger(f"Purchase | {hero.name} | {item_key} | price={item['price']}")
    return True
def sell_item(hero, items, logger=None):
    """Sell one item unit for half its listed price."""
    show_inventory(hero, items)
    if not hero.inventory:
        return False
    item_key = find_item_key(input("Item name or ID to sell: "), items)
    if item_key is None or hero.inventory.get(item_key, 0) <= 0:
        print("That item is not in your inventory.")
        return False
    item = items[item_key]
    if item_key in hero.equipped and hero.inventory[item_key] == 1:
        hero.unequip(item_key, items)
    hero.inventory[item_key] -= 1
    if hero.inventory[item_key] == 0:
        del hero.inventory[item_key]
    sell_price = item["price"] // 2
    hero.gold += sell_price
    print(f"Item sold. You received {sell_price} gold.")
    if logger:
        logger(f"Sale | {hero.name} | {item_key} | price={sell_price}")
    return True
def open_shop(hero, items, logger=None):
    """Run the shop menu until the user chooses to leave."""
    while True:
        print("\n===== Shop Menu =====")
        print("1. List items")
        print("2. Buy")
        print("3. Sell")
        print("4. Inventory")
        print("5. Leave shop")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                show_shop(items)
            elif choice == "2":
                buy_item(hero, items, logger)
            elif choice == "3":
                sell_item(hero, items, logger)
            elif choice == "4":
                show_inventory(hero, items)
            elif choice == "5":
                print("You left the shop.")
                return
            else:
                print("Invalid choice. Enter a number from 1 to 5.")
        except (InventoryFullError, NotEnoughGoldError) as error:
            print(str(error))
            if logger:
                logger(f"Shop error | {type(error).__name__} | {error}")

