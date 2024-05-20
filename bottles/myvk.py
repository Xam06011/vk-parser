from vkbottle import API
# import os
# from dotenv import load_dotenv
# import asyncio
# import json


class Api:
    def __init__(self, token) -> None:
        self.token = token
        self.api = API(token=token)
        return None
    
    async def getCity(self, city_name):
        res = await self.api.database.get_cities(q=city_name, country_id=1, count=1)
        return res.items[0].id

    async def get_info(self, q,  city_name=None, age_from=None, age_to=None):
        
        if city_name != None:
            city_id = await self.getCity(city_name)
        else:
            city_id = None


        res =  await self.api.users.search(q=q,
                                           city=city_id,
                                           age_from=age_from,
                                           age_to=age_to,
                                    sex=0,
                                    fields=['about', 'has_photo','universities', 'relatives', 'personal', 'city','photo_400_orig','schools', 'music', 'videos'])

        return res.json()
    
    async def getPosts(self, owner_id):

        res = await self.api.wall.get(owner_id=owner_id)

        return res.json()
        

    async def writeIntoFile(self, data):
        # dumpData = data
        file = open("bottles.json", "w")

        
        file.write(data)

        file.close()
        

        # if len(dumpData) > 0:
        #     file = open("bottles.json", "w")
        #     print(data)
        #     json.dump(dumpData, file)
        # else:
        #     print("Wall is empty")
        #     return


# async def main():
#     load_dotenv()
#     login = os.getenv("LOGIN")
#     token = os.getenv("TOKEN")
#     app_id = os.getenv("APP_ID")

#     api = Api(token=token)

#     # res = await api.get_info(q="Хамза Оздоев", age_from=19, age_to=25)

#     res = await api.getPosts(346598810)
#     # print(res)


#     await api.writeIntoFile(res)
#     return




# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
    