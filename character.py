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
        min=target-3
        max=target+3
        damage=random.randint(min,max)
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
        if self.xp>=self.level*100:
            self.Level_up()
    def Level_up(self):
        self.level=self.level+1
        self.hp_max=math.ceil(self.hp_max*1.15)
        self.hp=self.hp_max
        
            
            
            
            
            
        
