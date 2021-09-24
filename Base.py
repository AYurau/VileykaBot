import sqlite3
import random
import time

from out import output_info, del_result

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# Создание таблиц
cursor.execute('CREATE TABLE IF NOT EXISTS finds(ID TEXT, name TEXT, thing TEXT, place TEXT, contact TEXT, '
               'photo TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS await(req_id TEXT, chat_id TEXT, name TEXT, thing TEXT)')


async def add_info(lst):
    thing_id = random.randint(1, 999)
    while thing_id in cursor.fetchall():
        thing_id = random.randint(1, 999)
    lst.insert(0, thing_id)
    cursor.executemany("""INSERT INTO finds
                    (ID, name, thing, place, contact, photo)
                    VALUES (?, ?, ?, ?, ?, ?)""", (lst,))
    conn.commit()

    del lst
    print("Данные успешно вставлены в таблицу")


async def find_user(chat_id, finds):
    thing_in_base = []
    sql_select_query = """select * from finds where thing = ?"""
    cursor.execute(sql_select_query, (finds,))
    records = cursor.fetchall()
    try:
        for row in records:
            thing_in_base.append(row[0])
            thing_in_base.append(row[1])
            thing_in_base.append(row[2])
            thing_in_base.append(row[3])
            thing_in_base.append(row[4])
            thing_in_base.append(row[5])

    except IndexError:
        pass
    finally:
        await output_info(chat_id, thing_in_base)


async def remove_info(chat_id, id_element):
    info = cursor.execute('SELECT * FROM finds WHERE ID=?', (id_element,))
    if info.fetchone() is None:
        result = False
        await del_result(chat_id, result)
    else:
        sql_select_query = """delete from finds where ID = ?"""
        cursor.execute(sql_select_query, (id_element,))
        result = True
        await del_result(chat_id, result)
        conn.commit()


async def await_database(request):
    await_id = random.randint(1, 999)
    while await_id in cursor.fetchall():
        await_id = random.randint(1, 999)
    request.insert(0, await_id)
    cursor.executemany("""INSERT INTO await (req_id, chat_id, name, thing) VALUES (?, ?, ?, ?)""", (request,))
    conn.commit()
    request.clear()
    print("Данные успешно вставлены в таблицу для поиска")



