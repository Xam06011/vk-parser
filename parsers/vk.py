import json
import requests
class VKParser:
    def __init__(self):
        return None

    def parse_by_userid(self, user_id):
        TOKEN_USER = "vk1.a.k6y1UpSOvI-3eb6Av_MnqbMGnA9RL-EP7eDFEBcmvt7rxX9vmFOLrRbpclc8cvG7bfEyHKb6TD59Cyt5eqlQB_vpk3KYakJhamiFNIvamjNA-fEm8W3HJsrDzYu0M2TnvJQw3kE2sQugcwS2i6kjUj__l-EFpTMSTJ8sM5reDFXXCiAKGgB5Elc5408ck-ANC21Lmsq48wDW3dSlYD6DNA" #ваш токен
        VERSION = 5.199 #версися api vk
        DOMAIN = user_id #ваш domain

        # через api vk вызываем статистику постов
        response = requests.get('https://api.vk.com/method/wall.get',
        params={'access_token': TOKEN_USER,
                'v': VERSION,
                'domain': DOMAIN,
                'count': 10,
                'filter': str('owner')})

        data = response.json()['response']['items']

        file = open("file.json", "w")

        print(data)

        json.dump(data[0], file)
                