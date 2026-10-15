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
