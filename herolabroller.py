import random
import json
import re
from playbyposthelper import PlayByPostHelper


class Roller:
    
    helper = None

    characters = {}
    
    def load_characters(self):
        self.helper = PlayByPostHelper()
        self.helper.check_data()
        self.helper.load_user_token()
        self.helper.load_campaign()
        self.helper.load_campaign_roster()
        self.characters = self.helper.check_and_load_characters()

    
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
        #nw wp
        character = self.get_character(name)
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
                return
            current_num += 1
    
    def iterate_over_attacks(self, attacks: dict, name):
        attack_roll = self.generate_random_roll(20)
        attack_total = attacks['first']['modifier'] + attack_roll
        damage_roll = self.generate_random_roll(attacks['first']['damage_die'])
        damage_total =  damage_roll + attacks['first']['damage_modifier']
        print(name, " rolled a ", attack_roll, "for a total of:",attack_total, " and if it hits it does , ", damage_total, " from a roll of ", damage_roll, " and modifier:", attacks['first']['damage_modifier'])
        print("Do you want to do a second attack?")
        second_rep = input().lower()
        if second_rep == "y":
            attack_roll = self.generate_random_roll(20)
            attack_total = attacks['second']['modifier'] + attack_roll
            damage_roll = self.generate_random_roll(attacks['second']['damage_die'])
            damage_total =  damage_roll + attacks['second']['damage_modifier']
            print(name, " rolled a ", attack_roll, "for a total of:",attack_total, " and if it hits it does , ", damage_total, " from a roll of ", damage_roll, " and modifier:", attacks['second']['damage_modifier'])
        else:
            return
        print("Do you want to do a third attack?")
        third_rep = input().lower()
        if third_rep == "y":
            attack_roll = self.generate_random_roll(20)
            attack_total = attacks['third']['modifier'] + attack_roll
            damage_roll = self.generate_random_roll(attacks['third']['damage_die'])
            damage_total =  damage_roll + attacks['third']['damage_modifier']
            print(name, " rolled a ", attack_roll, "for a total of:",attack_total, " and if it hits it does , ", damage_total, " from a roll of ", damage_roll, " and modifier:", attacks['third']['damage_modifier'])
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
        
    
    def parse_attack_match(self, match: str) -> dict :
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
        character = self.get_character(name)
        items = character['export']['actors']['actor.1']['items']
        #as is for ability score
        abilities = self.get_item_by_type_for_character(items, "ab")
        
        ability_names = []
        for key in abilities.keys():
            ability_names.append(abilities[key]['name'])
        
        print("Which ability do you want to see? ")
        count = 1
        for ability_name in ability_names:
            print(count, ":", ability_name)
            count += 1
                    
        ability_num = int(input().lower())
        current_num = 1
        for key in abilities.keys():
            if ability_num == current_num:
                
                print(abilities[key]['name'])
                print(abilities[key]['description'])
            current_num += 1
    
    def list_feats(self, name):
        print(" in get feats")
        #ft

        character = self.get_character(name)
        items = character['export']['actors']['actor.1']['items']
        #as is for ability score
        feats = self.get_item_by_type_for_character(items, "ft")
        
        feat_names = []
        for key in feats.keys():
            feat_names.append(feats[key]['name'])
        
        print("Which ability do you want to see? ")
        count = 1
        for feat_name in feat_names:
            print(count, ":", feat_name)
            count += 1
                    
        ability_num = int(input().lower())
        current_num = 1
        for key in feats.keys():
            if ability_num == current_num:
                
                print(feats[key]['name'])
                print(feats[key]['description'])
            current_num += 1
    
    def get_character_name(self):
        roll_static = "What player do you want to roll for?"
        print(roll_static)
        current_num = 1
        for character in self.characters['characters']:
            print(current_num, ":", character['export']['actors']['actor.1']['name'])
            current_num += 1
            
        y = int(input().lower())
        print("Chosen = ", y)
        current_num = 1
        for character in self.characters['characters']:
            if current_num == y:
                return character['export']['actors']['actor.1']['name']
            current_num += 1
        
    
def main():
    print("What do you want to do? (S)ingle Roll, (I)nitiative, (Sa)ve, (Sk)ill Check, (AS)Ability Scores, (W)eapon Attacks, (SP)ecial Ability, (FT)Feats")

    x = input().upper()
    rl = Roller()
    rl.load_characters()
    
    
    
    if x == "S":
        name = rl.get_character_name()
        rl.single_roll(name)
    elif x == "I":
        
        rl.roll_initiative()
    elif x == "SA":
        name = rl.get_character_name()
        rl.roll_save(name)
    elif x == "SK":
        name = rl.get_character_name()
        rl.roll_skill_check(name)
    elif x == "AS":
        name = rl.get_character_name()
        rl.get_stats(name)
    elif x == "W":
        name = rl.get_character_name()
        rl.handle_attack(name)
    elif x == "SP":
        name = rl.get_character_name()
        rl.handle_special_ability(name)
    elif x == "FT":
        name = rl.get_character_name()
        rl.list_feats(name)

if __name__ == '__main__':
    main()



        
            



