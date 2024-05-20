from flask import Flask
import asyncio
from config import TOKEN
from myvk import Api

app = Flask(__name__)
api = Api(token=TOKEN)

async def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    

@app.route('/')
async def hello_world():
    res = await api.get_info(q="Хамза Оздоев", age_from=19, age_to=25)
    return res

async def main():
    app.run(host='0.0.0.0')
    



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())