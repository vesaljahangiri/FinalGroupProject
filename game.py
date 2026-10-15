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

    # ===== کنترل بازی =====
    def run(self):
        """کنترل بازی: منوی شروع و بعد گرفتن دستور ها"""
        self.start_menu()
        print("برای دیدن دستورها «راهنما» را بنویسید.")
        while self.running:
            command = input("\nدستور شما: ").strip()
            try:
                self.do_command(command)
            except InvalidCommandError:
                print("دستور نامعتبر است. برای دیدن دستورها «راهنما» را بنویسید.")
            except InvalidMoveError:
                print("از این طرف راهی نیست.")
            except InventoryFullError:
                print("کوله‌پشتی پر است! اول یک آیتم را دور بیندازید.")
            except NotEnoughGoldError:
                print("طلای کافی ندارید.")

    def do_command(self, command):
        """دستور رو اجرا میکنه"""
        if command in ["شمال", "n"]:
            self.move("شمال")
        elif command in ["جنوب", "s"]:
            self.move("جنوب")
        elif command in ["شرق", "e"]:
            self.move("شرق")
        elif command in ["غرب", "w"]:
            self.move("غرب")
        elif command == "نقشه":
            self.show_map()
        elif command == "فروشگاه":
            self.shop()
        elif command == "وضعیت":
            self.show_status()
        elif command == "ذخیره":
            self.save_menu()
        elif command == "رکوردها":
            self.show_leaderboard()
        elif command == "راهنما":
            self.show_help()
        elif command == "خروج":
            self.running = False
            print("خداحافظ!")
        else:
            raise InvalidCommandError()

    def show_help(self):
        """راهنمای دستور ها"""
        print("دستورها:")
        print("  شمال / جنوب / شرق / غرب  (یا n / s / e / w)  حرکت")
        print("  نقشه       نمایش نقشه")
        print("  فروشگاه    خرید و فروش (فقط در دهکده)")
        print("  وضعیت      نمایش وضعیت قهرمان")
        print("  ذخیره      ذخیره‌ی بازی در یکی از سه اسلات")
        print("  رکوردها    جدول برترین بازیکنان")
        print("  راهنما     همین لیست")
        print("  خروج       خروج از بازی")

    def start_menu(self):
        """منوی شروع بازی"""
        while True:
            print("\n===== منوی شروع =====")
            print("1. بازی جدید")
            print("2. ادامه‌ی بازی ذخیره‌شده")
            print("3. جدول رکوردها")
            choice = get_int("انتخاب شما: ", 1, 3)
            if choice == 1:
                self.new_game()
                return
            elif choice == 2:
                if self.load_menu():
                    return
                print("می‌توانید یک بازی جدید شروع کنید.")
            else:
                self.show_leaderboard()

    def new_game(self):
        """ساختن قهرمان جدید"""
        name = get_text("نام قهرمان: ")
        self.hero = Hero(name, START_HP, START_HP, START_ATTACK, START_DEFENCE)
        self.defeated = set()
        print("خوش آمدی", name + "! ماجراجویی از دهکده شروع می‌شود.")

    # ===== ذخیره =====
    def save_menu(self):
        """میپرسه کدوم اسلات و سیو میکنه"""
        self.show_slots()
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

    # ===== بارگذاری =====
    def show_slots(self):
        """نشون دادن اسلات ها"""
        for slot in range(1, 4):
            print("اسلات", slot, ":", self.slot_summary(slot))

    def slot_summary(self, slot):
        """میگه اسلات خالیه یا خرابه یا اسم و سطح قهرمان"""
        try:
            data = self.read_save_file(slot)
        except SaveFileError:
            return "خراب"
        if len(data) == 0:
            return "خالی"
        if "name" not in data or "level" not in data:
            return "خراب"
        return data["name"] + " - سطح " + data["level"]

    def load_menu(self):
        """میپرسه کدوم اسلات و لودش میکنه"""
        self.show_slots()
        slot = get_int("کدام اسلات بارگذاری شود؟ (1 تا 3): ", 1, 3)
        return self.load_game(slot)

    def read_save_file(self, slot):
        """فایل سیو رو میخونه و یه دیکشنری برمیگردونه"""
        file_name = SAVE_FILES[slot - 1]
        data = {}
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line == "":
                        continue
                    parts = line.split("|")
                    if len(parts) != 2:
                        raise SaveFileError()
                    data[parts[0].strip()] = parts[1].strip()
        except FileNotFoundError:
            open(file_name, "w", encoding="utf-8").close()
        return data

    def load_game(self, slot):
        """لود کردن بازی، اگه نشد False برمیگردونه"""
        try:
            data = self.read_save_file(slot)
            if len(data) == 0:
                print("اسلات", slot, "خالی است.")
                return False
            self.build_hero(data)
        except (SaveFileError, KeyError, ValueError):
            print("فایل ذخیره‌ی اسلات", slot, "خراب است و قابل بارگذاری نیست.")
            return False
        print("بازی", self.hero.name, "بارگذاری شد.")
        return True

    def build_hero(self, data):
        """ساختن دوباره قهرمان از روی فایل سیو"""
        for key in SAVE_KEYS:
            if key not in data:
                raise KeyError(key)
        hero = Hero(data["name"], int(data["hp"]), int(data["max_hp"]),
                    int(data["attack"]), int(data["defence"]))
        hero.level = int(data["level"])
        hero.xp = int(data["xp"])
        hero.gold = int(data["gold"])
        hero.position = text_to_position(data["position"])
        hero.inventory = text_to_inventory(data["inventory"])
        hero.visited = text_to_positions(data["visited"])
        if hero.hp <= 0 or hero.hp > hero.max_hp or hero.level < 1 or hero.gold < 0:
            raise ValueError("bad numbers")
        self.hero = hero
        self.defeated = text_to_positions(data["defeated"])

    # ===== جدول رکوردها =====
    def calculate_score(self):
        """حساب کردن امتیاز: سطح * 100 + طلا + جاهای دیده شده * 20"""
        hero = self.hero
        return hero.level * 100 + hero.gold + len(hero.visited) * 20

    def add_to_leaderboard(self):
        """اضافه کردن امتیاز به جدول"""
        score = self.calculate_score()
        line = self.hero.name + " | " + str(score) + " | " + str(self.hero.level)
        try:
            with open(LEADERBOARD_FILE, "a", encoding="utf-8") as file:
                file.write(line + "\n")
        except OSError:
            print("خطا: رکورد ذخیره نشد.")
        return score

    def read_leaderboard(self):
        """خوندن جدول رکورد ها از فایل"""
        records = []
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
                line_number = 0
                for line in file:
                    line_number = line_number + 1
                    line = line.strip()
                    if line == "":
                        continue
                    parts = line.split("|")
                    try:
                        records.append((int(parts[1]), parts[0].strip(), int(parts[2])))
                    except (IndexError, ValueError):
                        print("هشدار: خط", line_number, "فایل", LEADERBOARD_FILE, "نامعتبر بود و نادیده گرفته شد.")
        except FileNotFoundError:
            open(LEADERBOARD_FILE, "w", encoding="utf-8").close()
        return records

    def show_leaderboard(self):
        """نشون دادن 10 تا رکورد اول"""
        records = self.read_leaderboard()
        records.sort(reverse=True)
        print("\n===== برترین بازیکنان =====")
        if len(records) == 0:
            print("هنوز رکوردی ثبت نشده.")
            return
        rank = 1
        for score, name, level in records[:TOP_PLAYERS]:
            print(str(rank) + ".", name, "| امتیاز:", score, "| سطح:", level)
            rank = rank + 1

    def show_status(self):
        """نشون دادن وضعیت قهرمان"""
        hero = self.hero
        print(hero.name, "| جان:", hero.hp, "/", hero.max_hp, "| سطح:", hero.level,
              "| تجربه:", hero.xp, "| طلا:", hero.gold)
        print("کوله‌پشتی:", hero.inventory)

    def game_over(self, won):
        """آخر بازی: نشون دادن امتیاز و ثبت تو جدول"""
        if won:
            print("\nتبریک! غول آخر را شکست دادی!")
        else:
            print("\nقهرمان شکست خورد...")
        self.show_status()
        score = self.add_to_leaderboard()
        print("امتیاز نهایی:", score)
        self.show_leaderboard()
        self.running = False


def main():
    """شروع برنامه"""
    game = Game()
    game.run()


main()
