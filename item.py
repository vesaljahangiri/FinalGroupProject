items = {
    "item 1": {
        "name": "Sword",
        "type": "Weapon",
        "power": 50,
        "weight": 10,
        "price": 100
    },
    "item 2": {
        "name": "Shield",
        "type": "Defense",
        "power": 20,
        "weight": 15,
        "price": 80
    },
    "item 3": {
        "name": "Potion",
        "type": "Health",
        "power": 30,
        "weight": 1,
        "price": 50
    },
    "item 4": {
        "name": "Armor",
        "type": "Defense",
        "power": 40,
        "weight": 20,
        "price": 200
    }
}
#--------------------------------------------------------------------------------------------------------------#
inventory = {}
gold = 500
#-------------------------------------------------- SHOW SHOP --------------------------------------------------#
def Show_shop():
    print("---- SHOP ----")
    for item in items:
        print("Name:", items[item]["name"])
        print("Type:", items[item]["type"])
        print("Power:", items[item]["power"])
        print("Weight:", items[item]["weight"])
        print("Price:", items[item]["price"])
        print("------------------------")
#-------------------------------------------- SHOW INVENTORY ----------------------------------------------------#
def Show_inventory():
    print("----- INVENTORY ------")
    if len(inventory) == 0:
        print("Your inventory is empty")
    else:
        for item in inventory:
            print("Name:", items[item]["name"])
            print("Type:", items[item]["type"])
            print("Power:", items[item]["power"])
            print("Weight:", items[item]["weight"])
            print("Price:", items[item]["price"])
            print("count: " , inventory[item])
            print("------------------------")
#-------------------------------------------- BUY ITEM ----------------------------------------------------------#
def buy_item():
    global gold
    Show_shop()
    name=input("enter item name:").lower().strip()
    for item in items:
        if items[item]["name"].lower().strip() == name:
            if gold >= items[item]["price"]:
                gold = gold - items[item]["price"]
                if item in inventory:
                    inventory[item] = inventory[item] + 1
                else:
                    inventory[item] = 1
                print("purchase successfully")
            else:
                print("not enouth gold!")
            return
    print("item not found!")
#--------------------------------------------------- SELL ITEM -------------------------------------------------#
def sell_item():
    global gold
    Show_inventory()
    name= input("enter item name to sell: ").lower().strip()
    for item in inventory:
        if items[item]["name"].lower() == name:
            gold = gold + items[item]["price"]
            if item in inventory:
                inventory[item] = inventory[item] - 1

            if inventory[item] == 0:
                del inventory[item]
            print("item sold successfully")
            return
        print("item not found!")
#-----------------------------------------------------SAVE INVENTORY -----------------------------------------#
def save_inventory():
    file = open("inventory.txt" , "w")
    file.write(str(gold) + "\n")
    for item in inventory:
        file.write(item + "," + str(inventory[item]) + "\n")
    file.close()
    print("Inventory saved successfully!")
#------------------------------------------------------ LOAD INVENTORY ----------------------------------------#
def load_inventory():
    global gold , inventory 
    inventory = {}
    try:
        file = open("inventory.txt" , "r")
        gold = int(file.readline())
        for line in file:
            data = line.strip().split(",")
            inventory[data[0]] = int(data[1])
        file.close()
        print("inventory loaded successfully!")
    except FileNotFoundError:
        print("no saved inventory found!")
#-------------------------------------------------------- ADD ITEM -----------------------------------------------#
def add_item():
    name=input("enter item name: ").lower().strip()
    type=input("enter item type: ").lower().strip()
    power=int(input("enter item power: "))
    weight=int(input("enter item weight: "))
    price=int(input("enter item price: "))
    for item in items:
        if items[item]["name"].lower() == name.lower():
            print("This item already exists!")
            return
    number = len(items) + 1
    items["item " + str(number)] = {
        "name": name,
        "type": type,
        "power": power,
        "weight": weight,
        "price": price
    }
    print("item added successfully")
#------------------------------------------------------------ LOAD ITEMS ------------------------------------------#
def load_items():
    global items
    item = {}
    try:
        file = open("item.txt", "r")
        for line in file:
            data = line.strip().split(",")
            items[data[0]] = {"name": data[1] , "type": data[2] , "power": int(data[3]) ,
                            "weight": int(data[4]) , "price": int(data[5])}
        file.close()
        print("shop loaded successflly!")
    except FileNotFoundError:
        print("NO saved shop found!")
#------------------------------------------------------------ SAVE ITEM ------------------------------------------#
def save_items():
    file = open("item.txt" , "w")
    for item in items:
        file.write(item + "," + items[item]["name"] + "," +
                    items[item]["type"] + "," +
                    str(items[item]["power"]) + "," + 
                    str(items[item]["weight"]) + "," + 
                    str(items[item]["price"]) + "\n")
    file.close()
    print("shop saved successfully")
#------------------------------------------------------------------------------------------------------------------#
try:
    file=open("item.txt" , "r")
    file.close()
except FileNotFoundError:
    save_items()
#-------------------------------------------------- MENU ----------------------------------------------------------#
while 1:
    print("======= GAME MENU =======")
    print("1.Show Menu , 2.Show Inventory , 3.Buy Item , 4.Sell Item , 5.Show Gold , 6.Save Game , 7.Load Game , 8.Add Item to Shop , 9.Exit")
    code = input("choose code foe work: ").lower().strip()

    if code == "1":
        Show_shop()
    elif code == "2":
        Show_inventory()
    elif code == "3":
        buy_item()
    elif code == "4":
        sell_item()
    elif code == "5":
        print("count of gold =" , gold)
    elif code == "6":
        save_items()
        save_inventory()
    elif code == "7":
        load_items()
        load_inventory()
    elif code == "8":
        add_item()
    elif code == "9":
        print("finish your work")
        break
    else:
        print("error number!")
