import json
import requests
import asyncio
class VKParser:
    def __init__(self, TOKEN):
        self.TOKEN = TOKEN 
        self.VERSION = 5.199 #версися api vk
        return None
    
    async def get_city_by_name(self, city):

        response = requests.get('https://api.vk.com/method/database.getCities',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'q': city,
                'count' : 1
                })
        
        print(response.json())

        city_id = response.json()['response']['items'][0]['id']

        return city_id


    async def parse_by_user(self, user_name, city, age_from):
        DOMAIN = user_name #ваш domain
        city_id = None
        # Получаем id города
        if city != None:
            city_id = await self.get_city_by_name(city)

        # через api vk вызываем статистику постов
        response = requests.get('https://api.vk.com/method/users.search',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'q': DOMAIN,
                'city': city_id ,
                'age_from': age_from,
                'count': 10
                })

        
        # print(response.json())

        data = response.json()['response']['items']

        user_ids = []

        # for i in range(len(data)):
        #     user_ids[i] = data[i]['id']

        for item in data:
            user_ids.append(item['id'])

        print(user_ids)

        if len(data) > 0:
            file = open("file.json", "w")

            # print(data)

            json.dump(data, file)
        else:
            print("Wall is empty")
            return
        await self.parsebout(user_ids)
                
    async def parsebout(self, user_ids):

        user_ids = [str(element) for element in user_ids]

        print(user_ids)

        delimiter = ", "
        user_ids = delimiter.join(user_ids)

        # через api vk вызываем статистику постов
        response = requests.get('https://api.vk.com/method/users.get',
        params={'access_token': self.TOKEN,
                'v': self.VERSION,
                'user_ids': user_ids,
                'fields': ['about', 'has_photo','universities', 'relatives', 'personal', 'city', 'photo_400_orig', 'schools']
                })

        # print(json.dumps([470101470, 419020778, 275717499]))
        print(response.json()['response'])

        data = response.json()['response']
        if len(data) > 0:
            file = open("users_data.json", "w")

            print(data)

            json.dump(data, file)
        else:
            print("Wall is empty")
            return


TOKEN_USER = "vk1.a.k6y1UpSOvI-3eb6Av_MnqbMGnA9RL-EP7eDFEBcmvt7rxX9vmFOLrRbpclc8cvG7bfEyHKb6TD59Cyt5eqlQB_vpk3KYakJhamiFNIvamjNA-fEm8W3HJsrDzYu0M2TnvJQw3kE2sQugcwS2i6kjUj__l-EFpTMSTJ8sM5reDFXXCiAKGgB5Elc5408ck-ANC21Lmsq48wDW3dSlYD6DNA" #ваш токен
vk = VKParser(TOKEN_USER)


async def main():

    await vk.parse_by_user('Котикова', 'Ярославль', None)


if __name__ == "__main__":
    asyncio.run(main())