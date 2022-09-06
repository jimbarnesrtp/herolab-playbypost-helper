from os import access
import unittest
from playbyposthelper import PlayByPostHelper 

class TestHerolab(unittest.TestCase):
    
    def setUp(self):
        unittest.TestLoader.sortTestMethodsUsing = None
        self.func = PlayByPostHelper()
        
    def test(self):
        self.assertTrue(True)
    
    def test_check_data(self):
        status = self.func.check_data()
        print("Status:", status)
        self.assertGreater(len(status),0)
    
    def test_load_user_token(self):
        access_Token = self.func.load_user_token()
        print("accessToken:", access_Token)
        self.assertIsNotNone(access_Token)
    
    def test_load_uu_campaign(self):
        campaign_Token = self.func.load_campaign()
        print("CampaignToken:", campaign_Token)
        self.assertIsNotNone(campaign_Token)
    
    def test_load_uuu_load_campaign_roster(self):
        self.func.load_user_token()
        self.func.load_campaign()
        roster = self.func.load_campaign_roster()
        print("Roster:", roster)
        self.assertIsNotNone(roster)
        
    def test_load_uuuu_load_pcs(self):
        self.func.load_user_token()
        self.func.load_campaign()
        self.func.load_campaign_roster()
        characters = self.func.check_and_load_characters()
        print("characters:", len(characters))
        self.assertIsNotNone(characters)

if __name__ == '__main__':
    unittest.main()