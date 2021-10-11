import sqlite3
import random

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
    await check_await(lst)
    lst.clear()
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
        await remove_req(chat_id, id_element)
        sql_select_query = """delete from finds where ID = ?"""
        cursor.execute(sql_select_query, (id_element,))
        result = True
        await del_result(chat_id, result)
        conn.commit()


async def remove_req(chat_id, id_element):
    sql_select_query = """select * from finds where ID = ?"""
    cursor.execute(sql_select_query, (id_element,))
    records = cursor.fetchall()
    thing = records[0][2]
    sql_remove_req = """delete from await where chat_id = ? and thing = ?"""
    cursor.execute(sql_remove_req, (chat_id, thing), )
    conn.commit()


async def await_database(request):
    await_id = random.randint(1, 999)
    while await_id in cursor.fetchall():
        await_id = random.randint(1, 999)
    request.insert(0, await_id)
    cursor.executemany("""INSERT INTO await (req_id, chat_id, name, thing) VALUES (?, ?, ?, ?)""", (request,))
    conn.commit()
    print("Данные успешно вставлены в таблицу для поиска")


async def check_await(lst):
    check_result =[]
    sql_request = 'select * from await where thing =?'
    cursor.execute(sql_request,(lst[2],))
    records = cursor.fetchall()
    if len(records) != 0:
        for row in records:
            check_result.append(row[0])
            check_result.append(row[1])
            check_result.append(row[2])
            check_result.append(row[3])
        await output_info(check_result[1],lst)

