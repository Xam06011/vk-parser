import asyncio
import logging
import sys

from aiogram import F, Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from aiogram.utils.callback_answer import CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

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
    kb = callback.message.reply_markup
    # print(kb.__dict__)
    # kb.__dict__["inline_keyboard"][0][callback_data.id]["text"] = f"-{callback_data.id}-"
    for i in range(len(kb.__dict__["inline_keyboard"][0])):
        item = kb.__dict__["inline_keyboard"][0][i]
        cb = item.callback_data.split(":")[-1]
        print(cb)
        print(item)
        if cb == str(callback_data.id):
            item.text = f"-{i+1}-"
        else:
            item.text = f"{i+1}"

    await callback.answer('')
    await callback.message.edit_media(inline_message_id=str(callback.message.message_id), media= types.InputMediaPhoto(media=res['response'][0]["photo_200_orig"]) )
    await callback.message.edit_caption(inline_message_id=str(callback.message.message_id), caption=f'<b><a href="vk.com/id{callback_data.id}">{res['response'][0]['first_name'] + ' ' + res['response'][0]['last_name']}</a></b>\n\n<a href="vk.com/id">Получить отчет по странице</a>', 
                                        reply_markup=kb,parse_mode="HTML")

    pass


def users_keyboard(data, id = None):
    try:
        builder = InlineKeyboardBuilder()
        
        if len(data) > 1:
            for i in range(len(data)):
                builder.add(types.InlineKeyboardButton(
                    text=f"{i+1}",
                    callback_data=ChangeCallback(foo="ch_mess", index=i, id=data[i]).pack()
                    )
                )
        builder.row(types.InlineKeyboardButton(
                        text="Получить полный отчет о странице",
                        callback_data="1"
                    ))
        return builder.as_markup()
    except TypeError as err:
        print(err)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=
                                   [
                                       [
                                           types.KeyboardButton(text= "Начать поиск 🔍"),
                                           types.KeyboardButton(text = "Получить отчет по id 🆔")
                                       ]
                                   ])
    
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Данный бот предназначен для поиска информации о людях в социальной сети VK!", reply_markup=kb)


class ChooseData(StatesGroup):
    choosing_data_q = State()
    choosing_data_city = State()
    choosing_data_age_from = State()
    choosing_data_age_to = State()
    FIND_MATCHES = State()
    


@dp.message(F.text.lower().contains("начать поиск") or Command("find"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Введите имя и (или) фамилию человека:")

    await state.set_state(ChooseData.choosing_data_q)

@dp.message(ChooseData.choosing_data_q, F.text.func(len) >= 4)
async def q_chosen(message: Message, state: FSMContext):
    await state.update_data(choosing_data_q=message.text)
    
    await message.answer(text="Теперь введите город для поиска:")
    
    await state.set_state(ChooseData.choosing_data_city)

@dp.message(ChooseData.choosing_data_q)
async def q_chosen_incorrectly(message: Message):
    await message.answer(
        text="Минимальная длина имени 4 символа, попробуйте еще раз"
    )

@dp.message(ChooseData.choosing_data_city)
async def city_chosen(message: Message, state: FSMContext):
    
    await state.update_data(choosing_data_city=message.text)
    data = await state.get_data()
    print(data)
    
    await state.set_state(ChooseData.FIND_MATCHES)
    


@dp.message(ChooseData.FIND_MATCHES)
async def echo_handler(message: Message, state: FSMContext):
    try:
        
        # await state.set_data(FIND_MATCHES="")
        await message.answer(text="Начинаю поиск...")
        
        data = await state.get_data()
        res = await parser.userSearch(q=data["choosing_data_q"], city_name=data["choosing_data_city"])

        await message.answer(text="Было найдено " + str(len(res)) + " подходящих страниц:")
        if len(res) < 1:
            await state.clear()
            return
        user = await parser.userGet(str(res[0]))

        await message.answer_photo(
            photo= user["response"][0]["photo_200_orig"], 

            caption=f'<b><a href="vk.com/id{user['response'][0]['id']}">{user['response'][0]['first_name'] + ' ' + user['response'][0]['last_name']}</a></b>\n\n<a href="vk.com/id">Получить отчет по странице</a>', 

            reply_markup=users_keyboard(res),
            
            parse_mode="HTML"
            )
        await state.clear()
        
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