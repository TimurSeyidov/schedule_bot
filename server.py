import telebot
import functools
from datetime import datetime as dt
from typing import Dict
import re
from pprint import pprint
from dotenv import dotenv_values
from datetime import datetime
from telebot.types import Message, User, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, User

from src.models import Settings, Schedules
from src.classes import SubscriptionType

config = dotenv_values(".env")
bot = telebot.TeleBot(config.get('BOT_API_KEY'))

def log_decorator(func):
    @functools.wraps(func)
    def wrapper(obj: Message | User, *args, **kwargs):
        user = obj.from_user if isinstance(obj, Message) else obj
        print('[{}] {} - {} {}'.format(
            datetime.now(),
            user.id,
            user.username,
            func.__name__
        ))
        return func(obj, *args, **kwargs)
    return wrapper

@bot.message_handler(commands=['start'])
@log_decorator
def handle_start(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='🗓️ Расписание', callback_data='schedule'),
        InlineKeyboardButton(text='🛠️ Настройки', callback_data='settings'),
    )
    bot.send_message(message.chat.id, text='Выберите действие:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print(call)
    actions = {
        'start': lambda user, message: handle_start(message),
        'schedule': handle_schedule,
        'settings': handle_settings,
        '#schedule_(?P<id>\\d+)': handle_schedule_list
    }
    for action, callback in actions.items():
        if action.startswith('#'):
            action = action[1:]
            result = re.search(re.compile(action), call.data)
            if not result:
                continue
            opt = result.groupdict()
            return callback(call.from_user, call.message, opt)
        elif call.data == action:
            return callback(call.from_user, call.message)
    return None

def handle_schedule(user: User, message: Message):
    # На главный экран
    # Расписание - есть расписание
    # Настройки - нет расписания
    markup = InlineKeyboardMarkup()

    def response(text: str):
        markup.add(
            InlineKeyboardButton(text='⬅️ В начало', callback_data='start'),
        )
        return bot.send_message(message.chat.id, text=text, reply_markup=markup)

    subscribes = Settings.get_subscribe_by_user_id(user.id)
    if not subscribes:
        markup.add(
            InlineKeyboardButton(text='🛠️ Настройки', callback_data='settings'),
        )
        return response('У вас нет ни одной подписки.'
            +'Вы можете это сделать в разделе *Настройки*')
    for subscribe in subscribes:
        markup.add(
            InlineKeyboardButton(
                text=subscribe.name,
                callback_data=f'schedule_{subscribe.id}'
            )
        )
    return response('Выберите группу/преподавателя')

def handle_schedule_list(user: User, message: Message, opt: Dict = None):
    subscribe = Settings.get_subscribe_by_id(
        user_id=user.id,
        _id=int(opt.get('id'))
    )
    if not subscribe:
        bot.send_message(message.chat.id, text='Подписка не найдена')
        return handle_schedule(user, message)
    if subscribe.type == SubscriptionType.TEACHER:
        bot.send_message(message.chat.id, text='-')
        return handle_schedule(user, message)
    schedules = dict()
    now = dt.now().strftime('%Y-%m-%d')
    for schedule in filter(lambda s: s.date >= now, Schedules.get_items_by_group_id(subscribe.outer_id)):
        if not schedule.date in schedules:
            schedules[schedule.date] = list()
        schedules[schedule.date].append(schedule)
    for _date in sorted(schedules.keys()):
        text = []
        for schedule in sorted(schedules.get(_date, []), key=lambda s: s.position):
            text.append('*{}, {}*\n{} пара\n{}, {}'.format(
                schedule.date,
                subscribe.name,
                schedule.position,
                schedule.name,
                schedule.description
            ))
        bot.send_message(message.chat.id, text='\n\n'.join(text))
    return handle_schedule(user, message)


def handle_settings(user: User, message: Message):
    pass

#
# @bot.message_handler(commands=['info'])
# @log_decorator
# def handle_info(message: Message):
#     markup = InlineKeyboardMarkup()
#     markup.add(
#         InlineKeyboardButton(text='Google', url='https://google.com'),
#         InlineKeyboardButton(text='Github', url='https://github.com'),
#     )
#     markup.add(
#         InlineKeyboardButton(text='Callback button', callback_data='test')
#     )
#     bot.send_message(message.chat.id, 'Выберите сайт:', reply_markup=markup)
#
# @bot.message_handler(commands=['help'])
# @log_decorator
# def handle_help(message: Message):
#     help_text = """
#     Доступные команды:
#     /start - Начало работы
#     /help - Помощь
#     /info - Информация о боте
#     """
#     bot.reply_to(message, help_text)
#
# @bot.message_handler(commands=['photo'])
# @log_decorator
# def handle_photo(message: Message):
#     # with open('./assets/2130.jpg', 'rb') as photo:
#     photo = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS73eI9GY5VljceK7gsoIqS87H2s0R8RYxBYZQPzkb9kU1E2CMTQXSZGecS6tPKRm2SQ7s&usqp=CAU'
#     bot.send_photo(message.chat.id, photo, caption='Hihihi')
#
# @bot.message_handler(content_types=['text'])
# @log_decorator
# def handle_text(message: Message):
#     bot.reply_to(message, f"Вы написали: `{message.text}`")
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_handler(call):
#     if call.data == 'test':
#         bot.send_message(call.message.chat.id, "Вы нажали на кнопку с callback!")
#
#
# @bot.message_handler(content_types=['sticker'])
# @log_decorator
# def handle_sticker(message: Message):
#     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAANQaCwBUTJ0ayTBoW61FIai_fKUA90AAlldAAKezgsAAaIdftyZ8Zl3NgQ')


if __name__ == '__main__':
    print('Starting server')
    bot.infinity_polling()