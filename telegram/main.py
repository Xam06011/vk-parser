import asyncio
import logging
import sys

import requests

from aiogram import F, Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.utils.callback_answer import CallbackQuery
from aiogram.filters.callback_data import CallbackData


import vparser
import config

TOKEN = "7167534352:AAFLLQN-jHa-VAxVEg7mSJIQMQASKLGsxo8"
dp = Dispatcher()

class ChangeCallback(CallbackData, prefix="ch_mess"):
    foo: str
    index: int
    id : int 


@dp.callback_query(ChangeCallback.filter(F.foo == "ch_mess"))
async def changeMessage(callback: CallbackQuery, callback_data: ChangeCallback):

    res = await parser.userGet(str(callback_data.id))

    await callback.answer('')
    await callback.message.edit_media(inline_message_id=str(callback.message.message_id), media= types.InputMediaPhoto(media=res['response'][0]["photo_200_orig"]) )
    await callback.message.edit_caption(inline_message_id=str(callback.message.message_id), caption=f'<b><a href="vk.com/id{callback_data.id}">{res['response'][0]['first_name'] + ' ' + res['response'][0]['last_name']}</a></b>\n\n<a href="vk.com/id">Получить отчет по странице</a>', reply_markup=callback.message.reply_markup,parse_mode="HTML")

    pass


def users_keyboard(data):
    try:
        builder = InlineKeyboardBuilder()
        btns = []
        for i in range(len(data)):
            builder.add(types.InlineKeyboardButton(
                text=f"{i+1}",
                callback_data=ChangeCallback(foo="ch_mess", index=i, id=data[i]).pack()
                )
            )
        # builder = types.InlineKeyboardMarkup(
        #     [
        #         btns,
        #         [
        #             types.InlineKeyboardButton(
        #                 text="Получить полный отчет о странице",
        #                 callback_data=""
        #             )
        #         ]
                
        #     ]
        # )
        # builder.add(btns)
        builder.row(types.InlineKeyboardButton(
                        text="Получить полный отчет о странице",
                        callback_data="1"
                    ))
        return builder.as_markup()
    except TypeError as err:
        print(err)



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Данный бот предназначен для поиска информации о людях в социальной сети VK!")

@dp.message(Command("find"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Введите ниже данные о человеке: ФИО, возраст, город")






@dp.message(Command("user"))
async def echo_handler(message: Message) -> None:
    try:
        
        res = await parser.userSearch(q="Берс", city_name="Магас")

        await message.answer(text="Было найдено " + str(len(res)) + " подходящих страниц:")
        
        user = await parser.userGet(str(res[0]))

        await message.answer_photo(
            photo= user["response"][0]["photo_200_orig"], 

            caption=f'<b><a href="vk.com/id{user['response'][0]['id']}">{user['response'][0]['first_name'] + ' ' + user['response'][0]['last_name']}</a></b>\n\n<a href="vk.com/id">Получить отчет по странице</a>', 

            reply_markup=users_keyboard(res),
            
            parse_mode="HTML"
            )
        
    except TypeError:
        await message.answer("Nice try!")






@dp.message()
async def echo_handler(message: Message) -> None:

    print(message.text)
    try:
        await message.answer("Дик яр хьон вош")
    except TypeError:
        await message.answer("Nice try!")





async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    global parser
    parser = vparser.Parser(config.TOKEN)
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