class Guild:
    def __init__(self,name,rank,leader = None):
        self.name = name
        self.rank = rank
        self.leader = leader
        self.member = []
    
    def guild_info(self):
        print("---------------------------------Guild----------------------------------------")
        print(f"Name Guild: {self.name}")
        print(f"Rank Guild: {self.rank}")
        print(f"Leader Name: {self.leader.name}")
        print("--------------------------------Member----------------------------------------")
        print([f"Name: {i.name} Level: {i.level} Role: {i.role}"for i in self.member])
        
class  Player:
    def __init__(self,name,level,hp,role):
        self.name = name
        self.level = level
        self.hp = hp
        self.role = role
        self.weapon = None
        self.armor = None
    
    def player_info(self):
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}")
        print(f"Role: {self.role}")
        print(f"Weapon: {self.weapon.name_wp} rating: {self.weapon.rating} (Damage:{self.weapon.damage})")
        print(f"Armor: {self.armor.name_arm} rating: {self.armor.rating}  (Defense:{self.armor.defense}) ")
        print(f"-----------------------------------------------------------------------------")
        
class Weapons:
    def __init__(self,name_wp,damage,rating):
        self.name_wp = name_wp
        self.damage = damage
        self.rating = rating
    
    def drop_weapon():
        pass
    
    def state_weapon():
        pass

class Armors:
    def __init__(self,name_arm,defense,rating):
        self.name_arm = name_arm
        self.defense = defense
        self.rating = rating
        
    def drop_armor():
        pass
    
    def state_armor():
        pass

Dododuck = Guild('Dododuck','1')
Blackcat = Guild('Blackcat','2')

weapon1 = Weapons('Duskblade','10','C-')
weapon2 = Weapons('Angel Staff','200','B-')
weapon3 = Weapons('Bloodthirster','1500','A-')
weapon4 = Weapons('Runaan Hurricane','2500','A')

armor1 = Armors('Edge of Night','15','D+')
armor2 = Armors('Shroud of Stillness','100','C+')
armor3 = Armors('Berserker Armor','1500','A')
armor4 = Armors('Quickest Silver','1000','B+')

player1 = Player('Enzo','5','200','Assassin')
player1.weapon = weapon1
player1.armor = armor3

player2 = Player('Mei','10','290','Saint')
player2.weapon = weapon2
player2.armor = armor2

player3 = Player('Artti','15','450','Warrior')
player3.weapon = weapon3
player3.armor = armor3

player4 = Player('Finn','15','400','Archer')
player4.weapon = weapon4
player4.armor = armor4

player_list = [player1,player2,player3,player4]

Dododuck.leader = player3
Blackcat.leader = player4

Dododuck.member.append(player3)
Dododuck.member.append(player1)
Blackcat.member.append(player4)
Blackcat.member.append(player2)

guild_list =[Dododuck,Blackcat]

#Player
for i in player_list:
    i.player_info()
    
#Guild
for j in guild_list:
    j.guild_info()