import json
import requests
class VKParser:
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN 
        self.VERSION = 5.199 #версися api vk
        return None
    
    def get_city_by_name(self, city):

        response = requests.get('https://api.vk.com/method/database.getCities',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'q': city,
                'count' : 1
                })
        
        print(response.json())

        city_id = response.json()['response']['items'][0]['id']

        return city_id


    def parse_by_userid(self, user_name, city, age_from):
        DOMAIN = user_name #ваш domain

        # Получаем id города

        city_id = self.get_city_by_name(city)

        # через api vk вызываем статистику постов
        response = requests.get('https://api.vk.com/method/users.search',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'q': DOMAIN,
                'city': city_id,
                'age_from': age_from
                })

        
        print(response.json())

        data = response.json()['response']['items']
        if len(data) > 0:
            file = open("file.json", "w")

            print(data)

            json.dump(data, file)
        else:
            print("Wall is empty")
            return
                
    def parsebout(self, user_id):
        DOMAIN = user_id #ваш domain

        # через api vk вызываем статистику постов
        response = requests.get('https://api.vk.com/method/users.get',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'user_ids': DOMAIN,
                'fields': ['about', 'has_photo', 'relatives', 'personal']
                })

        
        print(response.json())

        # data = response.json()['response']['items']
        # if len(data) > 0:
        #     file = open("file.json", "w")

        #     print(data)

        #     json.dump(data, file)
        # else:
        #     print("Wall is empty")
        #     return


TOKEN_USER = "vk1.a.k6y1UpSOvI-3eb6Av_MnqbMGnA9RL-EP7eDFEBcmvt7rxX9vmFOLrRbpclc8cvG7bfEyHKb6TD59Cyt5eqlQB_vpk3KYakJhamiFNIvamjNA-fEm8W3HJsrDzYu0M2TnvJQw3kE2sQugcwS2i6kjUj__l-EFpTMSTJ8sM5reDFXXCiAKGgB5Elc5408ck-ANC21Lmsq48wDW3dSlYD6DNA" #ваш токен
vk = VKParser(TOKEN_USER)



vk.parse_by_userid('Хамзат Оздоев', "Магас", 39)