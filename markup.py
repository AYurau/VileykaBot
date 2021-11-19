from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Кнопка удаления вещи из базы
del_btn = InlineKeyboardButton('Это моё. Удалить запись.', callback_data='del_btn')
del_btn = InlineKeyboardMarkup().add(del_btn)

# Кнопка для заявки на поиск
await_btn = InlineKeyboardButton('Оставить заявку на поиск.', callback_data='await_btn')
await_btn = InlineKeyboardMarkup().add(await_btn)

# Кнопка назад
cancel_btn = InlineKeyboardButton('Назад', callback_data='cancel_btn')
cancel_btn = InlineKeyboardMarkup().add(cancel_btn)
