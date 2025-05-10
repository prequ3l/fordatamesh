import telebot
import datetime as dt
from deep_translator import GoogleTranslator
from datetime import datetime, timedelta
from telebot import types
from marks import Marks
from schedule import Schedule
from homeworks import Homeworks

bot = telebot.TeleBot('8035651260:AAFPxKORyIv0nhSSJoyf5rYYf1bECApvnds')
token: str = ''


@bot.message_handler(commands=['start'])
def start(message):
    url: str = "<a href='https://school.mos.ru/?backUrl=https%3A%2F%2Fschool.mos.ru%2Fv2%2Ftoken%2Frefresh'>ссылке</a>"

    bot.send_message(message.chat.id, '<i>Для начала работы с ботом нужен токен.</i>\n'
                                      '<b>Как его получить:</b>\n'
                                      f'<i>1. Перейдите по {url} и войдите.</i>\n'
                                      '<i>2. Скопируйте ваш токен и отправьте боту.</i>', parse_mode='html')
    bot.register_next_step_handler(message, get_token)

    try:
        bot.delete_message(message.chat.id, message.message_id - 1)
    except telebot.apihelper.ApiTelegramException:
        pass


def get_token(message):
    global token
    token = message.text.strip()

    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton('Оценки', callback_data='marks')
    btn_2 = types.InlineKeyboardButton('Расписание', callback_data='schedule')
    btn_3 = types.InlineKeyboardButton('ДЗ', callback_data='homeworks')
    markup.row(btn_1, btn_2, btn_3)

    bot.send_message(message.chat.id, 'Отлично, теперь выберите нужное', reply_markup=markup)

    try:

        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.delete_message(message.chat.id, message.message_id)
    except telebot.apihelper.ApiTelegramException:
        pass


def get_homework(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('НАЗАД', callback_data='homeworks'))

    date: str = message.text.strip().split('-')

    try:
        res_date: str = f'{date[0]}-{date[1].zfill(2)}-{date[2].zfill(2)}'
        homework: str = Homeworks(token).get_homework(res_date)
        if not homework:
            res: str = 'В ЭТОТ ДЕНЬ ДЗ НЕТ'
        else:
            res: str = f'ДЗ НА {res_date}\n{'-' * 100}\n{homework}'
    except IndexError:
        res: str = 'НЕПРАВИЛЬНЫЙ ФОРМАТ ДАТЫ'

    bot.send_message(message.chat.id, res, reply_markup=markup, parse_mode='html')

    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except telebot.apihelper.ApiTelegramException:
        pass


def main(message):
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton('Оценки', callback_data='marks')
    btn_2 = types.InlineKeyboardButton('Расписание', callback_data='schedule')
    btn_3 = types.InlineKeyboardButton('ДЗ', callback_data='homeworks')
    markup.row(btn_1, btn_2, btn_3)

    bot.send_message(message.chat.id, 'Выберите нужное', reply_markup=markup)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except telebot.apihelper.ApiTelegramException:
        pass


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'marks':
        markup = types.InlineKeyboardMarkup()
        btn_3 = types.InlineKeyboardButton('четвертные + годовые', callback_data='quarter n year')
        btn_1 = types.InlineKeyboardButton('за опр. четверть', callback_data='period_quarter')
        btn_2 = types.InlineKeyboardButton('за опр. полугодие', callback_data='period_half')
        btn_4 = types.InlineKeyboardButton('НА ГЛАВНУЮ', callback_data='return')
        markup.row(btn_1, btn_2)
        markup.row(btn_3)
        markup.row(btn_4)

        bot.send_message(callback.message.chat.id, 'Какие именно?', reply_markup=markup)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data == 'period_quarter':
        markup = types.InlineKeyboardMarkup()
        btn_1 = types.InlineKeyboardButton('1', callback_data='q1')
        btn_2 = types.InlineKeyboardButton('2', callback_data='q2')
        btn_3 = types.InlineKeyboardButton('3', callback_data='q3')
        btn_4 = types.InlineKeyboardButton('4', callback_data='q4')
        markup.row(btn_1, btn_2, btn_3, btn_4)

        bot.send_message(callback.message.chat.id, 'Выберите четверть', reply_markup=markup)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data.startswith('q') and len(callback.data) == 2:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('НАЗАД', callback_data='marks'))

        quarter_number: int = int(callback.data[-1])
        res: str = f'ОЦЕНКИ ЗА {quarter_number} ЧЕТВЕРТЬ\n{'-' * 100}\n{Marks(token).for_get_marks_quarter(quarter_number)}'

        bot.send_message(callback.message.chat.id, res, parse_mode='html', reply_markup=markup)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data == 'period_half':
        markup = types.InlineKeyboardMarkup()
        btn_1 = types.InlineKeyboardButton('1', callback_data='h1')
        btn_2 = types.InlineKeyboardButton('2', callback_data='h2')
        markup.row(btn_1, btn_2)

        bot.send_message(callback.message.chat.id, 'Выберите полугодие', reply_markup=markup)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data.startswith('h') and len(callback.data) == 2:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('НАЗАД', callback_data='marks'))

        quarter_number: int = int(callback.data[-1])
        res: str = f'ОЦЕНКИ ЗА {quarter_number} ПОЛУГОДИЕ\n{'-' * 100}\n{Marks(token).for_get_marks_half_year(quarter_number)}'

        bot.send_message(callback.message.chat.id, res, reply_markup=markup, parse_mode='html')

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data == 'quarter n year':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('НАЗАД', callback_data='marks'))

        res: str = f'ЧЕТВЕРТНЫЕ И ГОДОВЫЕ ОЦЕНКИ\n{'-' * 100}\n{Marks(token).for_get_quarter_and_year()}'

        bot.send_message(callback.message.chat.id, res, reply_markup=markup, parse_mode='html')

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data == 'return':
        main(callback.message)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data == 'schedule':
        markup = types.InlineKeyboardMarkup()
        btn_1 = types.InlineKeyboardButton('Понедельник', callback_data='sch_0')
        btn_2 = types.InlineKeyboardButton('Вторник', callback_data='sch_1')
        btn_3 = types.InlineKeyboardButton('Среда', callback_data='sch_2')
        btn_4 = types.InlineKeyboardButton('Четверг', callback_data='sch_3')
        btn_5 = types.InlineKeyboardButton('Пятница', callback_data='sch_4')
        btn_6 = types.InlineKeyboardButton('НА ГЛАВНУЮ', callback_data='return')
        markup.row(btn_1, btn_2)
        markup.row(btn_3, btn_4, btn_5)
        markup.row(btn_6)

        bot.send_message(callback.message.chat.id, 'Выберите день недели', reply_markup=markup)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data.startswith('sch_'):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('НАЗАД', callback_data='schedule'))

        day_number: int = int(callback.data[-1])
        days_ahead: int = day_number - datetime.today().weekday()

        if days_ahead <= 0:
            days_ahead -= 7

        res_date = datetime.today() + timedelta(days=days_ahead)
        res: str = Schedule(token).get_schedule(res_date.isoformat()[:10])

        while res == 'KeyError' or not res:
            res_date -= timedelta(days=7)
            res: str = Schedule(token).get_schedule(res_date.isoformat()[:10])

        name_date: str = dt.date(*list(map(int, res_date.isoformat()[:10].split('-')))).strftime("%A")
        translate_date: str = GoogleTranslator(source='en', target='ru').translate(name_date).upper()
        res = f'{translate_date} {res_date.isoformat()[:10]}\n{'-' * 100}\n{res}'

        bot.send_message(callback.message.chat.id, res, reply_markup=markup, parse_mode='html')

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data == 'homeworks':
        markup = types.InlineKeyboardMarkup()
        btn_1 = types.InlineKeyboardButton('На завтра', callback_data='homework_1')
        btn_2 = types.InlineKeyboardButton('Своя дата', callback_data='homework_2')
        btn_3 = types.InlineKeyboardButton('НА ГЛАВНУЮ', callback_data='return')
        markup.row(btn_1, btn_2)
        markup.row(btn_3)

        bot.send_message(callback.message.chat.id, 'Какое?', reply_markup=markup)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data == 'homework_1':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('НАЗАД', callback_data='homeworks'))

        date = datetime.today() + timedelta(days=1)

        homework: str = Homeworks(token).get_homework(date.isoformat()[:10])
        if not homework:
            res: str = 'НА ЗАВТРА ДЗ НЕТ'
        else:
            res = f'ДЗ НА ЗАВТРА\n{'-' * 100}\n{homework}'

        bot.send_message(callback.message.chat.id, res, reply_markup=markup, parse_mode='html')

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    if callback.data == 'homework_2':
        bot.send_message(callback.message.chat.id, '<i>Отправьте свою дату в формате:</i>\n<b>год-месяц-день</b>',
                         parse_mode='html')
        bot.register_next_step_handler(callback.message, get_homework)

        try:
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass


bot.polling(non_stop=True)
