import unittest
from herolabroller import Roller
from playbyposthelper import PlayByPostHelper

class TestHeroLabRoller(unittest.TestCase):
    
    
    def setUp(self):
        unittest.TestLoader.sortTestMethodsUsing = None
        self.func = Roller()
        self.helper = PlayByPostHelper()
        self.helper.check_data()
        characters = self.helper.check_and_load_characters()
        self.func.characters = characters
        
    def test(self):
        self.assertTrue(True)
        
    # def test_roll(self):
    #     roll = self.func.generate_random_roll()
    #     print("Roll:", roll)
    #     self.assertGreater(roll,0)
    
    # def test_get_character(self):
        
    #     character = self.func.get_character("Unach")
    #     self.assertIsNotNone(character)
    
    # def test_roll_init(self):
    #     self.func.roll_initiative()
    #     self.assertTrue(True)
    
    # def test_roll_save(self):
    #     self.func.roll_save("Unach")
    #     self.assertTrue(True)
        
    # def test_skill_check(self):
    #     self.func.roll_skill_check("Gwydd")
    #     self.assertTrue(True)
    
    # def test_get_stats(self):
    #     self.func.get_stats("Jorunn")
    #     self.assertTrue(True)
    
    # def test_get_weapons(self):
    #     attacks = self.func.parse_attacks("{b}Melee Strikes{/b} +7 / +3 / -1{br}{b}Melee Damage{/b} 1d4+3 P{br}{b}Melee Crit Damage{/b} \u00d72{br}{b}Range{/b} 10 ft.{br}{b}Ranged Strikes{/b} +7 / +3 / -1{br}{b}Ranged Damage{/b} 1d4+3 P{br}{b}Ranged Crit Damage{/b} \u00d72", "M")
    #     print(attacks)
    #     self.assertIsNotNone(attacks)
    
    # def test_get_weapons_2(self):
    #     attacks = self.func.parse_attacks("{b}Range{/b} 100 ft.{br}{b}Ranged Strikes{/b} +7 / +2 / -3{br}{b}Ranged Damage{/b} 1d8 P{br}{b}Ranged Crit Damage{/b} \u00d72 +1d10 P", None)
    #     print(attacks)
    #     self.assertIsNotNone(attacks)
    
    # def test_get_weapon_3(self):
    #     attacks = self.func.parse_attacks("{b}Melee Strikes{/b} +6 / +1 / -4{br}{b}Melee Damage{/b} 1d8+3 S{br}{b}Melee Crit Damage{/b} \u00d72", None)
    #     print(attacks)
    #     self.assertIsNotNone(attacks)

    def test_handle_attack(self):
        self.func.handle_attack("Jorunn")
        self.assertTrue(True)
    
        

if __name__ == '__main__':
    unittest.main()

