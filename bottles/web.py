from flask import Flask
import asyncio
from config import TOKEN
import myvk
import json
from vkbottle import API
app = Flask(__name__)


async def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
  
@app.route('/')
async def hello_world():
    res = await myvk.get_info(api, q="Хамза Оздоев", age_from=19, age_to=25)
    return json.loads(res)

async def main():
    global api
    api = API(token=TOKEN)
    app.run(host='localhost')
    

# main()

if __name__ == '__main__':
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_until_complete(main())
    # loop.run_forever()
    # loop.run_forever()
    # main()
    asyncio.run(main())