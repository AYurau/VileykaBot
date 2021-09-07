import sqlite3

from out import output_info

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute('CREATE TABLE IF NOT EXISTS finds(name TEXT, thing TEXT, place TEXT, contact TEXT, '
               'photo TEXT)')


async def add_info(lst):
    cursor.executemany("""INSERT INTO finds
                    (name, thing, place, contact, photo)
                    VALUES (?, ?, ?, ?, ?)""", (lst,))
    conn.commit()
    print("Данные успешно вставлены в таблицу")


def find_user(finds):
    thing_in_base = []
    sql_select_query = """select * from finds where thing = ?"""
    cursor.execute(sql_select_query, (finds,))
    records = cursor.fetchall()
    for row in records:
        thing_in_base.append(row[0])
        thing_in_base.append(row[1])
        thing_in_base.append(row[2])
        thing_in_base.append(row[3])
        thing_in_base.append(row[4])
    return thing_in_base





