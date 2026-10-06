import random
import math
class Character:
    def __init__(self,name,hp,max_hp,attack,defence):
        self.name=name
        self.hp=hp
        self.max_hp=max_hp
        self.attack=attack
        self.defence=defence
    def Is_alive(self):
        flag=False
        if self.hp<=0:
            self.hp=0
            print("you are dead")
        else:
            print("you are alive")
            flag=True
        return flag
    def Take_damage(self,amount):
        self.amount=amount
        self.hp=self.hp-self.amount
        self.Is_alive()
    def Attack_target(self,target):
        min=self.attack-3
        max=self.attack+3
        damage=random.randint(min,max)
        damage=damage-target.defence
        if damage<1:
            damage=1
        if random.randint(1,10)==1:
            damage=damage*2
            print("critical hit!")
            
        target.Take_damage(damage)
class Hero(Character):
    def __init__(self,name,hp,hp_max,attack,defence):
        super().__init__(name,hp,hp_max,attack,defence)
        self.xp=0
        self.gold=0
        self.level=1
        
        self.inventory={}
        self.position=(0,0)
        self.visited={(0,0)}
    def Gain_xp(self,amount):
        
        self.xp=self.xp+amount
        while self.xp>=self.level*100:
            self.xp=self.xp-self.level*100
            self.Level_up()
    def Level_up(self):
        self.level=self.level+1
        self.max_hp=math.ceil(self.hp_max*1.15)
        self.hp=self.hp_max
    def use_item(self,name_item,data_item):
        if name_item not in self.inventory:
            print("item not found")
            return
        else:
            item=data_item[name_item]
            if item["type"]=="heal":
                self.hp=self.hp+item["power"]
                if self.hp>self.max_hp:
                    self.hp=self.max_hp
            self.inventory[name_item]=self.inventory[name_item]-1
            if self.inventory[name_item]==0:
                del self.inventory[name_item]
            print("item used")
    def Equip(self,name_item,data_item):
        if name_item not in self.inventory:
                    print("item not found")
                    return
        item=data_item[name_item]
        if item["type"]=="armor":
            self.defence=self.defence+item["power"]
        elif item["type"]=="weapon":
            self.attack=self.attack+item["power"]
    def Inventory_weight(self,data_item):
        total=0
        for name_item,quantity in self.inventory.items():
            total=total+data_item[name_item]["weight"]*quantity
            
        return total
class Enemy(Character):
    def __init__(self,name,hp,max_hp,attack,defence,xp_reward,gold_reward):
        super().__init__(name,hp,max_hp,attack,defence)

        self.xp_reward=xp_reward
        self.gold_reward=gold_reward
            
        
class Boss(Enemy):
    def __init__(self,name,hp,max_hp,attack,defence,xp_reward,gold_reward):
        super().__init__(name,hp,max_hp,attack,defence,xp_reward,gold_reward)

        self.turn=0
     
            
            
            
        
