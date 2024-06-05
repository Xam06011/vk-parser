import requests
from jinja2 import Environment, PackageLoader, select_autoescape
import random

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

            city_id = response.json()['response']['items'][0]['id']

            return city_id
        
    
    async def userSearch(self, q, city_name = None, age_from = None, age_to = None):
        if city_name != None:
            city_id = await self.cityGet(city_name)
        else:
            city_id = None
        
        print(q, city_id, city_name)

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
                'fields': 'about, domain, photo_200_orig, photo_400_orig, city, personal, universities'
                })
        
        # print(response.json())
        
        return response.json()
    
    
    async def wallGet(self, owner_id = ""):
        
        response = requests.get('https://api.vk.com/method/wall.get',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'owner_id': owner_id,
                'count': 10
                })
        
        # print(response.json())
        
        return response.json()["response"]["items"]
    
    async def photosGet(self, owner_id = ""):
        response = requests.get('https://api.vk.com/method/photos.get',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'owner_id': owner_id,
                'album_id': 'wall'
                })
        
        # print(response.json())
        
        return response.json()["response"]["items"]
    
    async def genereteHtml(self, user_id):
        data = await self.userGet(user_ids=user_id)
        items = await self.wallGet(user_id)
        photos = await self.photosGet(user_id)
        
        env = Environment(
        loader=PackageLoader('html', 'templates'),
        autoescape=select_autoescape(['html'])
        )

        template = env.get_template('index.html')
        
        print(data)
        
        result = template.render(data = data["response"][0], items = items, photos = photos)
        
        filename = random.randint(1000000000, 999999999999)
        
        with open(f'./generated/{filename}.html', 'w') as fp: 
            fp.write(result)
        
        return f"{filename}.html"
    
    async def userGetAll():
        pass
        