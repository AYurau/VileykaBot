from main import bot


async def output_info(chat_id, thing_in_base):
    await bot.send_message(chat_id, text=f'Найден: {thing_in_base[2]}\nМесто: {thing_in_base[1]}\nКонтакты нашедшего: {thing_in_base[3]} {thing_in_base[0]}')
    await bot.send_photo(chat_id,photo=thing_in_base[4])
