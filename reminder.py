# Управление таймером
from datetime import datetime, date, time
from threading import Timer
import locale
import db_request


# Ставим локаль для правильного вывода месяца
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


# Считывание даты и времени
def get_datetime_reminder(string_time_reminder, string_date_reminder):
    def calculating_date_reminder():
        if string_date_reminder == '':
            return date.today()
        return date.fromisoformat(string_date_reminder)

    parsed_time_reminder = time.fromisoformat(string_time_reminder)
    parsed_date_reminder = calculating_date_reminder()
    string_datetime_reminder = str(datetime.combine(parsed_date_reminder, parsed_time_reminder))
    return string_datetime_reminder


# Считывание только времени
def get_message_time_reminder(string_datetime_reminder):
    datetime_reminder = datetime.fromisoformat(string_datetime_reminder)

    if datetime_reminder.day == datetime.today().day:
        time_remind = datetime_reminder.strftime('%H:%M')
        to_recap_message = 'Напомню сегодня в {}'.format(time_remind)
        return to_recap_message
    else:
        datetime_remind = datetime_reminder.strftime('%d %b, в %H:%M')
        to_recap_message = 'Напомню {}'.format(datetime_remind)
        return to_recap_message


# Берём время пользователя и вычитаем текущее время и из полученного высчитываем секунды
def get_timedelta(datetime_reminder):
    datetime_now = datetime.now()
    delta = datetime_reminder - datetime_now
    return delta.seconds


# Установка напоминания
def set_reminder(string_datetime_reminder, purchases, bot, chat_id):
    def remind(delay=False):
        inline_keyboard = purchases.create_inline_keyboard()
        bot.send_message(chat_id, 'Напоминаю про список',
                         reply_markup=inline_keyboard)

        connection, cursor = db_request.connect()
        sql_request = 'DELETE FROM reminder_purchase WHERE id=?;'
        cursor.execute(sql_request, (chat_id,))
        connection.commit()

        if delay is False:
            timer.cancel()

    datetime_reminder = datetime.fromisoformat(string_datetime_reminder)
    if datetime_reminder < datetime.now():
        remind(delay=True)
    else:
        time_delta = get_timedelta(datetime_reminder)
        timer = Timer(time_delta, remind)
        timer.start()


# Запись в бд
def write_data_reminder(string_datetime_reminder, chat_id):
    connection, cursor = db_request.connect()
    sql_request = 'INSERT INTO reminder_purchase VALUES (?, ?);'
    cursor.execute(sql_request, (string_datetime_reminder, chat_id))
    connection.commit()


# Чтение из бд
def read_data_reminder():
    connection, cursor = db_request.connect()
    sql_request = 'SELECT * FROM reminder_purchase;'
    cursor.execute(sql_request)
    return cursor.fetchall()