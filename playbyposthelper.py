from herolab import HeroLabHelper
from os.path import exists
import json
import os


class PlayByPostHelper:
    
    file_status = {}
    characters = {}
    campaign_key = {}
    characters_key = {}
    user_token = {}
    helper = HeroLabHelper()
    
    CHARACTERS_FILENAME = "characters-herolab.json"
    CHARACTERS_FLAG = "characters"
    CAMPAIGN_FILENAME = "campaign.json"
    CAMPAIGN_FLAG = "campaign"
    CHARACTER_ROSTER_FILENAME = "characterroster.json"
    CHARACTER_ROSTER_FLAG = "characterRoster"
    USER_TOKEN_FILENAME = "usertoken.json"
    USER_FLAG = "user"
    
    def check_data(self):
        directory_path = os.getcwd()
        if exists(directory_path+"/json/"+self.CHARACTERS_FILENAME):
            self.file_status['charactersPresent'] = True
        else:
            self.file_status['charactersPresent'] = False
        
        if exists(directory_path+"/json/"+self.CAMPAIGN_FILENAME):
            self.file_status['campaignPresent'] = True
        else:
            self.file_status['campaignPresent'] = False
        
        if exists(directory_path+"/json/"+self.CHARACTER_ROSTER_FILENAME):
            self.file_status['rosterPresent'] = True
        else:
            self.file_status['rosterPresent'] = False
        
        if exists(directory_path+"/json/"+self.USER_TOKEN_FILENAME):
            self.file_status['usertokenPresent'] = True
        else:
            self.file_status['usertokenPresent'] = False
        return self.file_status
            
    def load_json_file(self, file_name):
        directory_path = os.getcwd()
        with open(directory_path+"/json/"+file_name) as file:
            if file_name == self.CHARACTERS_FILENAME:
                self.characters = json.load(file)
            elif file_name == self.USER_TOKEN_FILENAME:
                self.user_token = json.load(file)
            elif file_name == self.CAMPAIGN_FILENAME:
                self.campaign_key = json.load(file)
            elif file_name == self.CHARACTER_ROSTER_FILENAME:
                self.characters_key = json.load(file)
                
    def load_user_token(self):
        if self.file_status['usertokenPresent']:
            self.load_json_file(self.USER_TOKEN_FILENAME)
        else:
            #your refresh token is stored
            print("Please enter your refresh token from herolab")
            x = input()
            self.user_token['accessToken'] = x
            self.store_data(self.USER_FLAG)
            
        return self.user_token
            
    def load_campaign(self):
        if self.file_status['campaignPresent']:
            self.load_json_file(self.CAMPAIGN_FILENAME)
        else:
            #the campaign key is found in herolab, by first going to the campaign you care about
            # click on settings on the left hand side
            # Click on integrate in the other section
            # click on get element token. on this page you can also get your user token
            print("Please Supply your element token for the campaign from herolab")
            y = input()
            self.campaign_key['campaignElement'] = y
            self.store_data(self.CAMPAIGN_FLAG)
            
        return self.campaign_key['campaignElement']
    
    def load_campaign_roster(self):
        if self.file_status['rosterPresent']:
            print("Do you want to refresh the character roster? (Y)es, (N)o")
            t = input().upper()
            if t == "Y":
                self.fetch_character_roster()

            else:
                self.load_json_file(self.CHARACTER_ROSTER_FILENAME)
        else:
            print("You have not loaded your character roster from herolab yet, do you want us to go fetch this? (Y)es, (N)o")
            t = input().upper()
            if t == "Y":
                self.fetch_character_roster()

        return self.characters_key
        
    
    def check_and_load_characters(self):
        if self.file_status['charactersPresent']:
            print("Do you want to refresh the characters? (Y)es, (N)o")
            t = input().upper()
            if t == "Y":
                self.fetch_characters()
            else:
                self.load_json_file(self.CHARACTERS_FILENAME)
        else:
            print("You have not loaded the characters, do you want to fetch this from herolab? (Y)es, (N)o")
            t = input().upper()
            if t == "Y":
                self.fetch_characters()
            else:
                self.load_json_file(self.CHARACTERS_FILENAME)
        return self.characters
    
    def load_data(self):
        
        self.load_user_token()
        self.load_campaign()
        self.load_campaign_roster()
        self.check_and_load_characters()    
        
        
            
    def fetch_character_roster(self):
        #print(self.user_token['accessToken'])
        self.helper.USER_KEY = self.user_token['accessToken']
        response = self.helper.get_campaign_pcs(self.campaign_key['campaignElement'])
        #print("In fetch:", response)
        self.characters_key = response
        
        self.store_data(self.CHARACTER_ROSTER_FLAG)

        
    def fetch_characters(self):
        self.helper.USER_KEY = self.user_token['accessToken']
        self.characters = self.helper.get_pc_data(self.campaign_key['campaignElement'],self.characters_key['castList'])
        self.store_data(self.CHARACTERS_FLAG)
        
        
        
    def store_data(self, data_to_store):
        print("saving ", data_to_store)
        if data_to_store == self.USER_FLAG:
            self.write_json(self.user_token, self.USER_TOKEN_FILENAME)
        elif data_to_store == self.CHARACTER_ROSTER_FLAG:
            self.write_json(self.characters_key, self.CHARACTER_ROSTER_FILENAME)
        elif data_to_store == self.CAMPAIGN_FLAG:
            self.write_json(self.campaign_key, self.CAMPAIGN_FILENAME)
        elif data_to_store == self.CHARACTERS_FLAG:
            self.write_json(self.characters, self.CHARACTERS_FILENAME)
    
    def write_json(self, data, name):
        directory_path = os.getcwd()
        json_data = json.dumps(data, indent=4)
        f = open(directory_path+"/json/"+name, "w")
        f.write(json_data)
        f.close()

def main():
    pl = PlayByPostHelper()
    pl.check_data()
    pl.helper = HeroLabHelper()
    pl.load_data()
    


if __name__ == '__main__':
    main()
    