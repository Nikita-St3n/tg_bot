from aiogram import Bot, Dispatcher, executor, types
# KEYBOARDS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
# LINKS
from tg_parser import get_anecdotes
# FSM
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
# TOKEN
# from dotenv import load_dotenv
# import os

#
# KEYBOARD
#

r_kb = ReplyKeyboardMarkup(resize_keyboard=True)
r_kb_1btn = KeyboardButton(text="/help") #помощь
r_kb_2btn = KeyboardButton(text="/content") #анекдоты
r_kb.add(r_kb_1btn).insert(r_kb_2btn)

i_kb = InlineKeyboardMarkup(row_width=1)
i_kb_1btn = InlineKeyboardButton(text="Анекдотов.нет", callback_data="anekdotov_net")
i_kb_2btn = InlineKeyboardButton(text="Скоро...", callback_data="soon")
i_kb_3btn = InlineKeyboardButton(text="Скоро...", callback_data="soon")
i_kb.add(i_kb_1btn, i_kb_2btn, i_kb_3btn)

# 
# FSM
# 

storage = MemoryStorage()
bot = Bot(token="6458916198:AAGtjpNbrrX8XKOUSak9rorLAIcee5gNja8", parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    page = State()

@dp.message_handler(commands="start") # Приветствие
async def start(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id,
                    text="Приветствую!\nВведите команду <b>/help</b>, чтобы получить инструкцию",
                    reply_markup=r_kb)
    
@dp.message_handler(commands="help") # Помощь
async def help(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id,
                    text="На данный момент доступны следующие команды:\n"\
                         "1) <b>/content</b> - выбрать сайт, с которого нужно будет взять информацию",
                    reply_markup=r_kb)

@dp.message_handler(commands="content") # Спрашиваем какой ресурс выбрать
async def get_page(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id,
                           text="Какой сайт выбираете?",
                           reply_markup=i_kb)
    
@dp.callback_query_handler(text="anekdotov_net") # Выбрали 1) Анекдотов.нет
async def anekdotov_net(cb: types.CallbackQuery):
    await cb.message.answer(text="Напишите страницу: 1...24",
                    reply_markup=r_kb)
    await UserState.page.set()

@dp.message_handler(state=UserState.page)
async def anekdots(msg: types.Message, state: FSMContext):
    await state.update_data(page=msg.text)
    page = await state.get_data()
    page = page['page']

    await state.finish()

    new_anekdots = get_anecdotes(page)
    await msg.answer(f"Страница №{page}")

    for url, text in new_anekdots.items():
        await bot.send_message(chat_id=msg.chat.id,
                               text=text['anekdot_text'],
                               reply_markup=r_kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
