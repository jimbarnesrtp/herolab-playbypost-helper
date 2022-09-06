import json
import requests

class HeroLabHelper:
    
    USER_KEY = "" 
    ACCESS_ENDPOINT = "https://api.herolab.online/v1/access/acquire-access-token"
    headers = {'Content-type': 'application/json', 'Accept': '*/*', 'User-Agent': 'Direrat-PBP'}

    
    PC_ENDPOINT = "https://api.herolab.online/v1/campaign/get-stage"
    BULK_ENDPOINT = "https://api.herolab.online/v1/character/get-bulk"
        
    def get_access_token(self):
        
        
        data = {
                'refreshToken': self.USER_KEY,
                'toolName': 'PlayByPost-direrat'
            }
        
        r = requests.post(url = self.ACCESS_ENDPOINT, json = data, headers=self.headers)
        
        print("status code:", r.status_code)
        response_data = json.loads(r.text)
        
        print("The response is:%s"%response_data)
        return response_data['accessToken']
    
    def get_campaign_pcs(self, campaign_token):
        
        access_token = self.get_access_token()
        
        data = {
            'accessToken': access_token,
            'campaignToken':  campaign_token
        }
        
        r = requests.post(url = self.PC_ENDPOINT, json = data, headers=self.headers)
        
        print("status code:", r.status_code)
        response_data = json.loads(r.text)
        
        print("The response is:%s"%response_data)
        
        cast_list = {
            
        }
        cast_list['castList'] = response_data['castList']
        
        return cast_list
    
    def get_pc_data(self, campaign, pc_list):
        access_token = self.get_access_token()
        
        data = {
            'accessToken': access_token,
            'characters': [] 
        }
        
        for pc in pc_list:
            new_character = {
                "elementToken": campaign,
                "castId": pc
            }
            data['characters'].append(new_character)
        #print("data to send:", data)
        r = requests.post(url = self.BULK_ENDPOINT, json = data, headers=self.headers)
        
        print("status code:", r.status_code)
        response_data = json.loads(r.text)
        
        #print("The response is:%s"%response_data)
        characters_resp = {}
        
        characters_resp['characters'] = response_data['characters']
        
        return characters_resp