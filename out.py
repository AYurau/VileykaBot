from main import bot

from markup import del_btn, await_btn


async def output_info(chat_id, thing_in_base):
    count_thing = 0
    if len(thing_in_base) == 0:
        await bot.send_message(chat_id, text=f'''К сожалению, предмет не найден в нашей базе!
                                                 Напишите /start для продолжения работы с ботом.''',reply_markup=await_btn)
    else:
        try:
            for info in range(0, len(thing_in_base), 6):
                await bot.send_photo(chat_id, photo=thing_in_base[info + 5],
                                     caption=f'''ID : {thing_in_base[info]}
                                                 Найден: {thing_in_base[info + 2]}
                                                 Место: {thing_in_base[info + 3]}
                                                 Контакты нашедшего: {thing_in_base[info + 4]} {thing_in_base[info + 1]}''',
                                     reply_markup=del_btn)

                count_thing += 1
            await bot.send_message(chat_id, text=f'''В базе {count_thing} найденных вещей по вашему запросу .
                                                     Если среди них есть ваша - свяжитесь с нашедшим.
                                                     Для продолжения работы с ботом напишите /start''')

        except IndexError:
            pass


async def del_result(chat_id, result):
    if result:
        await bot.send_message(chat_id, text=f'Запись удалена.\nДля продолжения работы с ботом - /start')
    else:
        await bot.send_message(chat_id, text=f'Запись с таким ID не найдена.\nДля продолжения работы с ботом - /start')



