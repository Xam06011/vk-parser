import requests

class Parser:
    
    def __init__(self, token) -> None:
        self.TOKEN = token
        self.VERSION = 5.199
        
    def userSeacrh(self, city):
        response = requests.get('https://api.vk.com/method/database.getCities',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'q': city,
                'count' : 1
                })
        
        print(response.json())

        city_id = response.json()['response']['items'][0]['id']

        return city_id