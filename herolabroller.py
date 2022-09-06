import random
import json

class Roller:

    characters = {}
    
    def generate_random_roll(self):
        a = random.randint(1,20)
        return a
        
    
    def get_character(self, name):
        print("Characters type:", type(self.characters))
        for character in self.characters['characters']:
            if character['export']['actors']['actor.1']['name'].upper().__contains__(name.upper()):
                return character
        return None
    
    def get_perception(self, items):
        for key in items.keys():
            if "perception".upper() in key.upper():
                return items[key]['stNet']
        return 0 
         
    
    def roll_initiative(self):
        for character in self.characters['characters']:
            roll = self.single_roll(character['export']['actors']['actor.1']['name'])
            #print("Roll is:", roll)
            perception = self.get_perception(character['export']['actors']['actor.1']['items'])
            #print(defense)
            total = roll + int(perception)
            print("Initiative for ", character['export']['actors']['actor.1']['name'], "is ", total, "from ", roll, " + ",  perception)
    
    def get_saves(self, items):
        saves = {}
        for key in items.keys():
            if key.startswith("sv"):
                saves[items[key]['name'].replace(" Save","")] = items[key]
                
        return saves
    
    def roll_save(self, name):
        roll = self.generate_random_roll()
        character = self.get_character(name)
        saves = self.get_saves(character['export']['actors']['actor.1']['items'])
        print("What Save are you wanting to roll on? (R)eflex, (F)ortitude, (W)ill")
        char_name = character['export']['actors']['actor.1']['name']
        save = input().upper()
        if save == "R":
            total = roll + saves['Reflex']['stNet']
            print("Reflex save for ", char_name, "is ", total, "from ", roll, " + ",  saves['Reflex']['stNet'])
        elif save == "F":
            total = roll + saves['Fortitude']['stNet']
            print("Fortitude save for ", char_name, "is ", total, "from ", roll, " + ",  saves['Fortitude']['stNet'])
        elif save == "W":
            total = roll + saves['Will']['stNet']
            print("Will save for ", char_name, "is ", total, "from ", roll, " + ",  saves['Will']['stNet'])
    
    def get_skills(self, items):
        skills = {}
        for key in items.keys():
            if key.startswith("sk"):
                skills[items[key]['name']] = items[key]
                
        return skills
    
    
    def roll_skill_check(self, name):
        roll = self.generate_random_roll()
        character = self.get_character(name)
        print("What skill do you want to check?")
        skills = self.get_skills(character['export']['actors']['actor.1']['items'])
        keys = skills.keys()
        print(keys)
        skill_name = input().lower()
        skill_to_check = {}
        for key in keys:
            if key.lower() == skill_name:
                skill_to_check = skills[key]
        total = roll + skill_to_check['stNet']
        print(skill_to_check['name'], " check for ", character['export']['actors']['actor.1']['name'], "is ", total, "from ", roll, " + ",  skill_to_check['stNet'], "Skill is :", skill_to_check['ProfLevel'])
        

    def single_roll(self, name):
        roll = self.generate_random_roll()
        
        print("Roll for ", name, " is ", roll)
        return roll

    
def main():
    print("What do you want to do? (S)ingle Roll, (I)nitiative, (Sa)ve, (Sk)ill Check, (A)pply Buff, Apply (C)ondition, Clear (St)atus")
    roll_static = "What player do you want to roll for?"
    x = input().upper()
    rl = Roller()
    rl.load_rolls()
    rl.load_characters()
    
    if x == "S":
        print(roll_static)
        y = input().lower()
        rl.single_roll(y)
    elif x == "I":
        
        rl.roll_initiative()
    elif x == "SA":
        print(roll_static)
        y = input().lower()
        rl.roll_save(y)
    elif x == "SK":
        print(roll_static)
        y = input().lower()
        rl.roll_skill_check(y)
    elif x == "A":
        print(roll_static)
        y = input().lower()
        rl.apply_buff(y)
    elif x == "C":
        print(roll_static)
        y = input().lower()
        rl.apply_debuff(y)
    elif x == "ST":
        print(roll_static)
        y = input().lower()
        rl.clear_conditions(y)
        
        
       
    rl.write_file()
    


if __name__ == '__main__':
    main()



        
            



