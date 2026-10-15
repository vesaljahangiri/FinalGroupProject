from character import Hero

# ثابت ها
SAVE_FILES = ["save_1.txt", "save_2.txt", "save_3.txt"]
LEADERBOARD_FILE = "leaderboard.txt"
TOP_PLAYERS = 10
START_HP = 100
START_ATTACK = 10
START_DEFENCE = 3
SAVE_KEYS = ["name", "hp", "max_hp", "attack", "defence", "level", "xp",
             "gold", "position", "inventory", "visited", "defeated"]


# خطا های بازی
class InvalidCommandError(Exception):
    """وقتی دستور اشتباه وارد بشه"""
    pass


class InventoryFullError(Exception):
    """وقتی کوله پشتی پر باشه"""
    pass


class NotEnoughGoldError(Exception):
    """وقتی طلا کم باشه"""
    pass


class InvalidMoveError(Exception):
    """وقتی از اون طرف راه نباشه"""
    pass


class SaveFileError(Exception):
    """وقتی فایل سیو خراب باشه"""
    pass


# تابع های کمکی
def get_int(prompt, min_value, max_value):
    """عدد میگیره و تا وقتی درست وارد نشه دوباره میپرسه"""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("چیزی وارد نکردید، دوباره امتحان کنید.")
            continue
        try:
            number = int(text)
        except ValueError:
            print("لطفاً فقط عدد وارد کنید.")
            continue
        if number < min_value or number > max_value:
            print("عدد باید بین", min_value, "تا", max_value, "باشد.")
            continue
        return number


def get_text(prompt):
    """یه متن میگیره که خالی نباشه و | نداشته باشه"""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("نمی‌تواند خالی باشد.")
        elif "|" in text:
            print("از علامت | استفاده نکنید.")
        else:
            return text


def position_to_text(position):
    """(0, 1) رو میکنه "0,1" """
    return str(position[0]) + "," + str(position[1])


def text_to_position(text):
    """متن "0,1" رو میکنه (0, 1)"""
    parts = text.split(",")
    if len(parts) != 2:
        raise ValueError("bad position")
    return (int(parts[0]), int(parts[1]))


def positions_to_text(positions):
    """set مختصات ها رو میکنه متن مثل "0,0;0,1" """
    parts = []
    for position in positions:
        parts.append(position_to_text(position))
    return ";".join(parts)


def text_to_positions(text):
    """متن "0,0;0,1" رو برمیگردونه به set"""
    positions = set()
    if text == "":
        return positions
    for part in text.split(";"):
        positions.add(text_to_position(part))
    return positions


def inventory_to_text(inventory):
    """کوله پشتی رو میکنه متن مثل "potion:2" """
    parts = []
    for item_name, count in inventory.items():
        parts.append(item_name + ":" + str(count))
    return ",".join(parts)


def text_to_inventory(text):
    """متن "potion:2" رو برمیگردونه به دیکشنری"""
    inventory = {}
    if text == "":
        return inventory
    for part in text.split(","):
        item_name, count = part.split(":")
        inventory[item_name] = int(count)
    return inventory


# ---------- کلاس اصلی بازی ----------
class Game:
    """کلاس اصلی بازی"""

    def __init__(self):
        self.hero = None
        self.defeated = set()   # جاهایی که دشمنش کشته شده
        self.running = True
        # world و بقیه رو بچه ها اضافه میکنن

    # ===== ذخیره =====
    def save_menu(self):
        """میپرسه کدوم اسلات و سیو میکنه"""
        slot = get_int("در کدام اسلات ذخیره شود؟ (1 تا 3): ", 1, 3)
        self.save_game(slot)

    def save_game(self, slot):
        """سیو کردن بازی تو اسلات"""
        hero = self.hero
        lines = [
            "name | " + hero.name,
            "hp | " + str(hero.hp),
            "max_hp | " + str(hero.max_hp),
            "attack | " + str(hero.attack),
            "defence | " + str(hero.defence),
            "level | " + str(hero.level),
            "xp | " + str(hero.xp),
            "gold | " + str(hero.gold),
            "position | " + position_to_text(hero.position),
            "inventory | " + inventory_to_text(hero.inventory),
            "visited | " + positions_to_text(hero.visited),
            "defeated | " + positions_to_text(self.defeated),
        ]
        try:
            with open(SAVE_FILES[slot - 1], "w", encoding="utf-8") as file:
                file.write("\n".join(lines) + "\n")
            print("بازی در اسلات", slot, "ذخیره شد.")
        except OSError:
            print("خطا: ذخیره انجام نشد.")
