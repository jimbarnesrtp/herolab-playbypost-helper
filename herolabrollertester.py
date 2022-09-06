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
        
    def test_roll(self):
        roll = self.func.generate_random_roll()
        print("Roll:", roll)
        self.assertGreater(roll,0)
    
    def test_get_character(self):
        
        character = self.func.get_character("Unach")
        self.assertIsNotNone(character)
    
    def test_roll_init(self):
        self.func.roll_initiative()
        self.assertTrue(True)
    
    def test_roll_save(self):
        self.func.roll_save("Unach")
        self.assertTrue(True)
        
    def test_skill_check(self):
        self.func.roll_skill_check("Gwydd")
        self.assertTrue(True)
        

if __name__ == '__main__':
    unittest.main()

