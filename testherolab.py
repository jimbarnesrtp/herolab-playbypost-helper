import unittest
from herolab import HeroLabHelper

class TestHerolab(unittest.TestCase):
    
    def setUp(self):
        unittest.TestLoader.sortTestMethodsUsing = None
        self.func = HeroLabHelper()
    
    def test(self):
        self.assertTrue(True)
        
    def test_get_access_token(self):
        data = self.func.get_access_token()
        self.assertIsNotNone(data)
        
    def test_get_pcs(self):
        data = self.func.get_campaign_pcs("$tDlbBtm~@P2#")
        self.assertGreaterEqual(len(data), 1)
    
    def test_get_pcs_data(self):
        castlist = [
            "m9BKthBj",
            "mBBFbzqR",
            "mXBPDE73",
            "moBoIFKA",
            "mRAh7Mvu",
            "mlBZKa8i"
        ]
        data = self.func.get_pc_data("$tDlbBtm~@P2#", castlist)
        self.assertGreaterEqual(len(data['characters']),1)
        
if __name__ == '__main__':
    unittest.main()