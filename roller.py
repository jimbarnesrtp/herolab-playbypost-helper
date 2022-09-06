import random
import json

class Roller:

    rollers = []
    characters = {}

    def load_rolls(self):
        file1 = open('rolls.csv', 'r')
        Lines = file1.readlines()
        
        # Strips the newline character
        for line in Lines:
            rolls = line.split(",")
            self.rollers.append(rolls)
        file1.close()
        
    def load_characters(self):
        with open("characters.json") as file:
            self.characters = json.load(file)
    
    def generate_random_roll(self, name):
        roll = -1
        for item in self.rollers:
            if item[0] == name.lower():
                if(len(item) < 2):
                    print("Name:", name, " is out of rolls")
                    return None
                a = random.randint(1,len(item)-1)
                roll = int(item.pop(a))
                return roll
        
        if roll == -1:
            print("User is not found!,", name)
            return None

    def write_file(self):
        file2 = open('rolls.csv', 'w')
        for line in self.rollers:
            string = ",".join(str(x) for x in line)
            file2.write(string)
        file2.close
    
    
    def get_character(self, name):
        for character in self.characters['players']:
            if character['player'] == name:
                return character
        return None
    
    def roll_initiative(self):
        for character in self.characters['players']:
            roll = self.single_roll(character['player'])
            #print("Roll is:", roll)
            defense = character['defenses']
            #print(defense)
            total = roll + int(defense['perception'])
            print("Initiative for ", character['characterName'], "is ", total, "from ", roll, " + ",  defense['perception'])
    
    def roll_save(self, name):
        roll = self.generate_random_roll(name)
        character = self.get_character(name)
        print("What Save are you wanting to roll on? (R)eflex, (F)ortitude, (W)ill")
        save = input().upper()
        if save == "R":
            total = roll + character['defenses']['reflex']
            print("Reflex save for ", character['characterName'], "is ", total, "from ", roll, " + ",  character['defenses']['reflex'])
        elif save == "F":
            total = roll + character['defenses']['fort']
            print("Fortitude save for ", character['characterName'], "is ", total, "from ", roll, " + ",  character['defenses']['fort'])
        elif save == "W":
            total = roll + character['defenses']['will']
            print("Will save for ", character['characterName'], "is ", total, "from ", roll, " + ",  character['defenses']['will'])
    
    def roll_skill_check(self, name):
        roll = self.generate_random_roll(name)
        character = self.get_character(name)
        print("What skill do you want to check?")
        print(character['skills'])
        skill_name = input().lower()
        skill_to_check = {}
        for skill in character['skills']:
            if skill['name'] == skill_name:
                skill_to_check = skill
        total = roll + skill_to_check['value']
        print(skill_name, " check for ", character['characterName'], "is ", total, "from ", roll, " + ",  skill_to_check['value'], "Skill is :", skill_to_check['level'])
        

    def single_roll(self, name):
        roll = self.generate_random_roll(name)
        
        if roll is not None:
            self.write_file()
            print("Roll for ", name, " is ", roll)
        else:
            print("Name:", name, " could not be found")
        return roll
    
    def load_buffs(self):
        with open("buffs.json") as file:
            buffs = json.load(file)
        
        return buffs

    def load_debuffs(self):
        with open("debuffs.json") as file:
            debuffs = json.load(file)
        
        return debuffs
    
    def apply_buff(self, name):
        character = self.get_character(name)
        buffs = self.load_buffs()
        print(buffs)
        print("what buff do you want to apply?")
        y = input()
        for buff in buffs['list']:
            if buff['name'] == y:
                character['buffs'].append(buff)
        self.save_characters()
    
    def apply_debuff(self, name):
        character = self.get_character(name)
        debuffs = self.load_debuffs()
        print(debuffs)
        print("what debuff do you want to apply?")
        y = input()
        for debuff in debuffs['list']:
            if debuff['name'] == y:
                print("What Level of the Debuff?")
                debuff['level'] = input()
                character['debuffs'].append(debuff)
        self.save_characters()
        
    def clear_conditions(self, name):
        character = self.get_character(name)
        character['buffs'] = []
        character['debuffs'] = []
        self.save_characters()
        
    def save_characters(self):

        json_data = json.dumps(self.characters, indent=4)
#       print(json_data)
        filename = "characters.json"
        f = open(filename, "w")
        f.write(json_data)
        f.close

    
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



        
            



