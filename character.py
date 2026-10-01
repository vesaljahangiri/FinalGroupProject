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
    def take_damage(self,amount):
        self.amount=amount
        self.hp=self.hp-self.amount
        self.Is_alive()
            
            
            
            
            
        
