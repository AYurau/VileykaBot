import random

from Base import add_info, find_user
from main import bot, dp
from aiogram import types, executor
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class u_info(StatesGroup):
    thing = State()
    place = State()
    photo = State()
    contact = State()


class user_find(StatesGroup):
    thing_f = State()


lst = []


@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Привет. Я - телеграм бот, который помогает жителям '
                                                              'г.Вилейка искать то, что они теряют. А тем, кто нашёл '
                                                              'чужую вещь - скорее найти владельца. Скажи, как тебя '
                                                              'зовут?')


@dp.message_handler(content_types=['text'])
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup()
    but_1 = InlineKeyboardButton('Да,я нашёл!', callback_data='but_1')
    but_2 = InlineKeyboardButton('Нет, я потерял.', callback_data='but_2')
    markup.add(but_1, but_2)
    lst.append(message.text)
    await bot.send_message(chat_id=message.from_user.id, text=f'Очень приятно, {message.text}. Ты что-то нашёл?',
                           reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == "but_1")  # Действие для нашедшего
async def form(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='1.Скажи, что ты нашел?\n(Просто название предмета. '
                                                              'Например: телефон, кошелёк, карта)')
    await u_info.thing.set()


@dp.callback_query_handler(lambda c: c.data == "but_2")  # Действие для поиска
async def finder(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='1.Скажи, что ты потерял?\n(Просто название предмета. '
                                                              'Например: телефон, кошелёк, карта)')
    await user_find.thing_f.set()


@dp.message_handler(state=u_info.thing)  # Ответ на вопрос 1(вещь)
async def th_form(message: types.Message, state: FSMContext):
    answer = message.text
    lst.append(str(answer).capitalize())
    await bot.send_message(chat_id=message.from_user.id, text='2.Скажи, где и когда ты это обнаружил?\n(Примерное '
                                                              'время и место)')
    await u_info.place.set()


@dp.message_handler(state=u_info.place)  # Ответ на вопрос 2(время место)
async def pl_form(message: types.Message, state: FSMContext):
    answer = message.text
    lst.append(str(answer))
    await bot.send_message(chat_id=message.from_user.id, text='3.Напиши, пожалуйста, свой номер для связи')
    await u_info.contact.set()


@dp.message_handler(state=u_info.contact)  # Ответ на вопрос 3(контакт)
async def ct_form(message: types.Message, state: FSMContext):
    answer = message.text
    lst.append(str(answer))
    await bot.send_message(chat_id=message.from_user.id, text='4.Загрузи, пожалуйста, фото находки:')
    await u_info.photo.set()


@dp.message_handler(content_types=['photo'], state=u_info.photo)
async def photo_answer(message, state: FSMContext):
    doc_id = message.photo[0].file_id
    lst.append(doc_id)
    await state.update_data(photo_f=doc_id)
    await state.finish()
    await add_info(lst)


@dp.message_handler(state=user_find.thing_f)  # Поиск вещи
async def ct_form(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup()
    answer = message.text
    finds = str(answer).capitalize()
    thing_in_base = find_user(finds)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Найден: {thing_in_base[2]}\nМесто: {thing_in_base[1]}\nКонтакты нашедшего: {thing_in_base[3]} {thing_in_base[0]}')
    await bot.send_photo(chat_id=message.from_user.id, photo=thing_in_base[4])
    but_3 = InlineKeyboardButton('Это моё!\nЯ уже связался с нашедшим!', callback_data='but_3')
    markup.add(but_3)

    await state.finish()


executor.start_polling(dp)
