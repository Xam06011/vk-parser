import requests

class Parser:
    
    def __init__(self, token) -> None:
        self.TOKEN = token
        self.VERSION = 5.199

    async def cityGet(self, city):
        response = requests.get('https://api.vk.com/method/database.getCities',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'q': city,
                'count' : 1
                })
        
        # print(response.json())

        city_id = response.json()['response']['items'][0]['id']

        return city_id
    
    async def userSearch(self, q, city_name = None, age_from = None, age_to = None):
        if city_name != None:
            city_id = await self.cityGet(city_name)
        else:
            city_id = None

        response = requests.get('https://api.vk.com/method/users.search',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'q': q,
                'city': city_id ,
                'age_from': age_from,
                'age_to': age_to,
                'count': 10
            }).json()
        print(123)
        user_ids = [str(item["id"]) for item in response["response"]["items"]]
        print(user_ids)
        return user_ids
    
    async def userGet(self, user_ids = ""):
        if len(user_ids) == 0:
            return None
        
        response = requests.get('https://api.vk.com/method/users.get',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'user_ids': user_ids,
                'fields': ['about', 'has_photo','universities', 'relatives', 'personal', 'city', 'photo_400_orig', 'schools','photo_200_orig']
                })
        
        print(response.json())
        
        return response.json()
        