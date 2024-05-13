from vkbottle import API
import os
from dotenv import load_dotenv
import asyncio
import json

async def get_info(token):
    api = API(token=token)

    res =  await api.users.search(q="Берс ПОлонкоев",fields=['about', 'has_photo','universities', 'relatives', 'personal', 'city','photo_400_orig','schools', 'music', 'video'], name_case=None)

    

    return res

async def writeIntoFile(data):
    # dumpData = data
    file = open("bottles.json", "w")

    
    file.write(data.json())



    # if len(dumpData) > 0:
    #     file = open("bottles.json", "w")
    #     print(data)
    #     json.dump(dumpData, file)
    # else:
    #     print("Wall is empty")
    #     return


async def main():
    load_dotenv()
    login = os.getenv("LOGIN")
    token = os.getenv("TOKEN")
    app_id = os.getenv("APP_ID")

    res = await get_info(token)

    # print(type(res[0]))
    # res[0] = list(res[0])
    # print(type(res[0]))
    # print(res[0])

    # d = {}

    # for i in list(res[0]):
    #     dict[str(i[0])] = i[1]



    await writeIntoFile(res)
    return




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    