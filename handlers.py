import markup

from Base import add_info, find_user, remove_info, await_database
from main import bot, dp
from aiogram import types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class u_info(StatesGroup):
    start = State()
    thing = State()
    place = State()
    photo = State()
    contact = State()


class user_find(StatesGroup):
    thing_f = State()


class remove_thing(StatesGroup):
    remove = State()


class await_thing(StatesGroup):
    user_name = State()
    user_thing = State()


lst = []
req_lst = []


@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Привет. Я - телеграм бот, который помогает жителям '
                                                              'г.Вилейка искать то, что они теряют. А тем, кто нашёл '
                                                              'чужую вещь - скорее найти владельца.'
                                                              'Если вы нашли какую-ошибку в работе бота - '
                                                              'пожалуйста напишите мне @kishevatov\n'
                                                              'Скажите, как вас зовут?')


@dp.message_handler(content_types=['text'])
async def name(message: types.Message):
    lst.clear()
    markup = InlineKeyboardMarkup()
    but_1 = InlineKeyboardButton('Да,я нашёл!', callback_data='but_1')
    but_2 = InlineKeyboardButton('Нет,я потерял.', callback_data='but_2')
    markup.add(but_1, but_2)
    lst.append(message.text)
    await bot.send_message(chat_id=message.from_user.id, text=f'Очень приятно, {message.text}. Вы что-то нашли?',
                           reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == "but_1")  # Действие для нашедшего
async def form(message: types.Message):
    message_obj = await bot.send_message(chat_id=message.from_user.id, text='1.Скажите, что вы нашли?\n(Просто '
                                                                            'название предмета. '
                                                                            'Например: телефон, кошелёк, карта)',
                                         reply_markup=markup.cancel_btn)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_obj.message_id - 1)
    await message.answer()
    await u_info.thing.set()


@dp.callback_query_handler(lambda c: c.data == "but_2")  # Действие для поиска
async def finder(message: types.Message):
    message_obj = await bot.send_message(chat_id=message.from_user.id, text='1.Скажите, что вы потеряли?\n(Просто '
                                                                            'название предмета. '
                                                                            'Например: телефон, кошелёк, карта)',
                                         reply_markup=markup.cancel_btn)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_obj.message_id - 1)
    await message.answer()
    await user_find.thing_f.set()


@dp.callback_query_handler(lambda c: c.data == "del_btn")  # Действие для удаления
async def copy_info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Введите ID находки, которую хотите удалить: ')
    await message.answer()
    await remove_thing.remove.set()


@dp.callback_query_handler(lambda c: c.data == "await_btn")  # Действие для запроса
async def await_request(message: types.Message, state: FSMContext):
    await state.finish()
    chat_user = message.from_user.id
    req_lst.append(chat_user)
    await bot.send_message(chat_id=message.from_user.id, text='1.Скажите, как вас зовут?')
    await await_thing.user_name.set()
    await message.answer()


@dp.callback_query_handler(lambda c: c.data == "cancel_btn", state=u_info.thing)  # Действие для возврата
async def cancel_thing(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Привет. Я - телеграм бот, который помогает жителям '
                                'г.Вилейка искать то, что они теряют. А тем, кто нашёл '
                                'чужую вещь - скорее найти владельца.'
                                'Если вы нашли какую-то ошибку в работе бота - '
                                'пожалуйста напишите мне @kishevatov\n'
                                'Скажите, как вас зовут?')
    await state.finish()


@dp.message_handler(state=remove_thing.remove)
async def remove_element(message: types.Message, state: FSMContext):
    id_element = message.text
    await remove_info(message.from_user.id, id_element)
    await state.finish()


@dp.message_handler(state=u_info.thing)  # Ответ на вопрос 1(вещь)
async def th_form(message: types.Message, state: FSMContext):
    answer = message.text
    lst.append(str(answer).capitalize())
    await bot.send_message(chat_id=message.from_user.id, text='2.Скажите, где и когда вы это обнаружили?\n(Примерное '
                                                              'время и место)')
    await u_info.place.set()


@dp.message_handler(state=u_info.place)  # Ответ на вопрос 2(время место)
async def pl_form(message: types.Message, state: FSMContext):
    answer = message.text
    lst.append(str(answer))
    await bot.send_message(chat_id=message.from_user.id, text='3.Напишите, пожалуйста, свой номер для связи')
    await u_info.contact.set()


@dp.message_handler(state=u_info.contact)  # Ответ на вопрос 3(контакт)
async def ct_form(message: types.Message, state: FSMContext):
    answer = message.text
    lst.append(str(answer))
    await bot.send_message(chat_id=message.from_user.id, text='4.Загрузите, пожалуйста, фото находки:')
    await u_info.photo.set()


@dp.message_handler(content_types=['photo'], state=u_info.photo)
async def photo_answer(message, state: FSMContext):
    doc_id = message.photo[0].file_id
    lst.append(doc_id)
    await bot.send_message(chat_id=message.from_user.id, text='Ваша находка успешно внесена в базу!\nКак только '
                                                              'хозяин увидит информацию о ней, он сразу с вами '
                                                              'свяжеться.\nПожалуйста, остерегайтесь мошенников и '
                                                              'передавайте находку только в том случае, если точно '
                                                              'уверены , что перед вами владелец.\nЕсли вы ещё что-то '
                                                              'нашли или потеряли, пожалуйста, напишите /start')
    await add_info(lst)
    lst.clear()
    await state.finish()


@dp.message_handler(state=user_find.thing_f)  # Поиск вещи
async def ct_form(message: types.Message, state: FSMContext):
    answer = message.text
    finds = str(answer).capitalize()
    chat_id = message.from_user.id
    await find_user(chat_id, finds)
    await state.finish()


@dp.message_handler(state=await_thing.user_name)  # Имя для запроса
async def await_name(message: types.Message, state: FSMContext):
    answer = message.text
    req_lst.append(answer)
    await bot.send_message(chat_id=message.from_user.id, text='2.Скажите, что вы потеряли?\n(Просто название предмета. '
                                                              'Например: телефон, кошелёк, карта)')
    await await_thing.user_thing.set()


@dp.message_handler(state=await_thing.user_thing)  # Вещь для запроса
async def await_name(message: types.Message, state: FSMContext):
    answer = message.text
    req_lst.append(answer)
    await bot.send_message(chat_id=message.from_user.id, text='Ваш запрос в базе!\nКак-только что-то появиться по '
                                                              'вашему запросу - мы вам напишем.\nДля продолжения '
                                                              'работы /start')
    await state.finish()
    await await_database(req_lst)
    req_lst.clear()


executor.start_polling(dp)
