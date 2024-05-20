import asyncio
import logging
import sys

import requests

from aiogram import Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message



# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7167534352:AAFLLQN-jHa-VAxVEg7mSJIQMQASKLGsxo8"
31
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# global api

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Данный бот предназначен для поиска информации о людях в социальной сети VK!")

@dp.message(Command("find"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Введите ниже данные о человеке: ФИО, возраст, город")

@dp.message(Command("user"))
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    res = requests.get("http://localhost:5000")
    # print(res.json())
    try:
        text = res.text()
        print(text)
        await message.answer(text=text)
    except TypeError:
        await message.answer("Nice try!")

@dp.message()
async def echo_handler(message: Message) -> None:

    print(message.text)
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        await message.answer("Дик яр хьон вош")
    except TypeError:
        await message.answer("Nice try!")





async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    # load_dotenv()
    # token = os.getenv("TOKEN")
    
    # global api
    # api = Api(token=token)
    await dp.start_polling(bot)
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())