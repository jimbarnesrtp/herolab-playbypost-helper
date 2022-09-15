import random
import json
import re

class Roller:

    characters = {}
    
    def generate_random_roll(self, bound):
        a = random.randint(1,bound)
        return a
        
    
    def get_character(self, name):
        #print("Characters type:", type(self.characters))
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
    
    def roll_save(self, name):
        roll = self.generate_random_roll(20)
        character = self.get_character(name)
        saves = self.get_item_by_type_for_character(character['export']['actors']['actor.1']['items'], "sv")
        print("What Save are you wanting to roll on? (R)eflex, (F)ortitude, (W)ill")
        char_name = character['export']['actors']['actor.1']['name']
        save = input().upper()
        if save == "R":
            total = roll + saves['Reflex Save']['stNet']
            print("Reflex save for ", char_name, "is ", total, "from ", roll, " + ",  saves['Reflex Save']['stNet'])
        elif save == "F":
            total = roll + saves['Fortitude Save']['stNet']
            print("Fortitude save for ", char_name, "is ", total, "from ", roll, " + ",  saves['Fortitude Save']['stNet'])
        elif save == "W":
            total = roll + saves['Will Save']['stNet']
            print("Will save for ", char_name, "is ", total, "from ", roll, " + ",  saves['Will Save']['stNet'])
    
    
    def roll_skill_check(self, name):
        roll = self.generate_random_roll(20)
        character = self.get_character(name)
        print("What skill do you want to check?")
        skills = self.get_item_by_type_for_character(character['export']['actors']['actor.1']['items'], "sk")
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
        roll = self.generate_random_roll(20)
        
        print("Roll for ", name, " is ", roll)
        return roll

    def get_stats(self, name):
        character = self.get_character(name)
        print("Stats for ", name)
        items = character['export']['actors']['actor.1']['items']
        #as is for ability score
        stats = self.get_item_by_type_for_character(items, "as")
        for key in stats.keys():
            if "stAbScModifier" in stats[key]:
                print(stats[key]['name'], "is ", stats[key]['stNet'], " with modifier:", stats[key]['stAbScModifier'])
            else:
                print(stats[key]['name'], "is ", stats[key]['stNet'], " with modifier: 0")
        
    
    def get_item_by_type_for_character(self, items, type):
        holder = {}
        for key in items.keys():
            if key.startswith(type):
                holder[items[key]['name']] = items[key]
                
        return holder
    
    def handle_attack(self, name: str):
        print("In get weapons")
        #nw wp
        character = self.get_character(name)
        print("Stats for ", name)
        items = character['export']['actors']['actor.1']['items']
        #as is for ability score
        weapons = self.get_item_by_type_for_character(items, "wp")
        
        weapon_names = []
        for key in weapons.keys():
            weapon_names.append(weapons[key]['name'])
        
        print("Which Weapon do you want to roll on? ")
        count = 1
        for weapon_name in weapon_names:
            print(count, ":", weapon_name)
            count += 1
                    
        weapon_num = int(input().lower())
        current_num = 1
        for key in weapons.keys():
            if weapon_num == current_num:
                count = weapons[key]['useInPlay'].count("Strikes")
                attack_type = None
                if count == 2:
                    print("This weapon can be used in (M)elee or (R)anged, which are you using?")
                    attack_type = input().upper()
                attacks = self.parse_attacks(weapons[key]['useInPlay'], attack_type)
                self.iterate_over_attacks(attacks, name)
                
            current_num += 1
    
    def iterate_over_attacks(self, attacks: dict, name):
        attack_roll = attacks['first']['modifier'] + self.generate_random_roll(20)
        damage_roll = self.generate_random_roll(attacks['first']['damage_die']) + attacks['first']['damage_modifier']
        print(name, " rolled a ", attack_roll, " and if it hits it does , ", damage_roll)
        print("Do you want to do a second attack?")
        second_rep = input().lower()
        if second_rep == "y":
            attack_roll = attacks['second']['modifier'] + self.generate_random_roll(20)
            damage_roll = self.generate_random_roll(attacks['second']['damage_die']) + attacks['second']['damage_modifier']
            print(name, " rolled a ", attack_roll, " and if it hits it does , ", damage_roll)
        else:
            return
        print("Do you want to do a third attack?")
        third_rep = input().lower()
        if third_rep == "y":
            attack_roll = attacks['third']['modifier'] + self.generate_random_roll(20)
            damage_roll = self.generate_random_roll(attacks['third']['damage_die']) + attacks['third']['damage_modifier']
            print(name, " rolled a ", attack_roll, " and if it hits it does , ", damage_roll)
        else:
            return
        
        
    def parse_attacks(self, attacks: str, attack_type):
        parsed_attacks = {}
        
        roll_matches = re.findall(".\d \/ .\d \/ .\d", attacks)
        damage_matches = re.findall("\dd\d+[/+/-]?\d?", attacks)
        print("Damage:", damage_matches)
        if attack_type is None or attack_type == "M":
            parsed_attacks = self.parse_attack_match(roll_matches[0])
            parsed_attacks = self.add_damage_to_attacks(parsed_attacks, damage_matches[0])
        elif attack_type == "R":
            parsed_attacks = self.parse_attack_match(roll_matches[1])
            parsed_attacks = self.add_damage_to_attacks(parsed_attacks, damage_matches[1])

        
        return parsed_attacks
    
    def add_damage_to_attacks(self, parsed_attacks: dict, damage_match: str):
        die = re.findall("d\d+", damage_match)[0].replace("d","")
        modifier_find = re.findall("[/+-]\d", damage_match)
        if len(modifier_find) == 0:
            modifier = 0
        else:
            modifier = int(modifier_find[0])
        
        for key in parsed_attacks.keys():
            parsed_attacks[key]['damage_die'] = int(die)
            parsed_attacks[key]['damage_modifier'] = modifier
        return parsed_attacks
        
    
    def parse_attack_match(self, match: str) -> list :
        parsed_attacks = {}
        attack_names = ['first', 'second', 'third']
        ats = match.split("/")
        
        count = 0
        for attack in ats:
            
            attack_dict = {}
            attack_dict['modifier'] = int(attack)
            parsed_attacks[attack_names[count]] = attack_dict
            count += 1
        return parsed_attacks
                    
                
            
        
    def handle_special_ability(self, name: str):
        print("In special abilities")
        #ab 
    
    def list_feats(self, name):
        print(" in get feats")
        #ft

    
def main():
    print("What do you want to do? (S)ingle Roll, (I)nitiative, (Sa)ve, (Sk)ill Check, (AS)Ability Scores")
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
    elif x == "AS":
        print(roll_static)
        y = input().lower()
        rl.get_stats(y)
        
        
       
    rl.write_file()
    


if __name__ == '__main__':
    main()



        
            



