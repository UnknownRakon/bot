# Фунцкии для манипуляции с бд
import sqlite3


def connect():
    connection = sqlite3.connect('friday.db')
    cursor = connection.cursor()
    return (connection, cursor)


def write_purchase(purchases, chat_id):
        connection, cursor = connect()
        sql_request = 'INSERT INTO purchase (purchase_list, id) VALUES (?, ?);'
        cursor.execute(sql_request, (purchases, chat_id))
        connection.commit()

def read_purchase(chat_id):
    connection, cursor = connect()
    sql_request = 'SELECT purchase_list FROM purchase WHERE id=?;'
    cursor.execute(sql_request, (chat_id, ))
    return cursor.fetchall()[0][0]

# Удаления элемента списка
def update_purchase(purchases, chat_id):
    connection, cursor = connect()
    sql_request = 'UPDATE purchase SET purchase_list=? WHERE id=?;'
    cursor.execute(sql_request, (purchases, chat_id))
    connection.commit()

# Удаление всего списка в базе
def delete_purchase(chat_id):
    connection, cursor = connect()
    sql_request = 'DELETE FROM purchase WHERE id=?;'
    cursor.execute(sql_request, (chat_id,))
    connection.commit()