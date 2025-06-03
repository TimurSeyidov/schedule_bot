import os
import telebot
import functools
from datetime import datetime as dt
from typing import Dict
import re
from pprint import pprint
from datetime import datetime
from src import Config, DbManager
from telebot.types import Message, User, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, User

from src.models import Settings, Schedules, Groups
from src.classes import SubscriptionType

config = Config('.env', start_path=os.path.abspath('./'))
db = DbManager(config)
bot = telebot.TeleBot(config.bot_api_key)
db.create_tables()
session = db.session
try:
    Groups.load_fake_data(session)
except:
    pass

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
        'subscribe': handle_subscribe,
        'subscribe_groups': handle_subscribe_groups,
        'subscribe_teacher': handle_subscribe_teacher,
        '#schedule_(?P<id>\\d+)': handle_schedule_list,
        '#settings_(?P<id>\\d+)$': handle_settings_operation,
        '#settings_(?P<id>\\d+)_remove$': handle_settings_remove,
        '#subscribe_groups_(?P<id>\\d+)$': handle_subscribe_group,
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
        bot.send_message(message.chat.id,
                         text='\n\n'.join(text),
                         parse_mode='Markdown'
                         )
    return handle_schedule(user, message)

def handle_settings(user: User, message: Message):
    markup = InlineKeyboardMarkup()
    subscribes = Settings.get_subscribe_by_user_id(user.id)
    for subscribe in subscribes:
        markup.add(
            InlineKeyboardButton(
                text=subscribe.name,
                callback_data=f'settings_{subscribe.id}'
            )
        )
    markup.add(
        InlineKeyboardButton(text='🆕 Подписаться', callback_data='subscribe'),
        InlineKeyboardButton(text='⬅️ В начало', callback_data='start'),
    )
    return bot.send_message(message.chat.id, text='Выберите действие', reply_markup=markup)

def handle_settings_operation(user: User, message: Message, opt: Dict = None):
    subscribe = Settings.get_subscribe_by_id(
        user_id=user.id,
        _id=int(opt.get('id'))
    )
    if not subscribe:
        bot.send_message(message.chat.id, text='Подписка не найдена')
        return handle_settings(user, message)
    markup = InlineKeyboardMarkup()
    text = subscribe.name + '\n*Удалить?*'
    markup.add(
        InlineKeyboardButton(text='✅ Да', callback_data=f'settings_{subscribe.id}_remove'),
        InlineKeyboardButton(text='❌ Нет', callback_data='settings'),
    )
    return bot.send_message(chat_id=message.chat.id,
                            text=text,
                            reply_markup=markup,
                            parse_mode='Markdown'
                            )

def handle_settings_remove(user: User, message: Message, opt: Dict = None):
    subscribe = Settings.get_subscribe_by_id(
        user_id=user.id,
        _id=int(opt.get('id'))
    )
    if subscribe:
        # удаляем подписку
        bot.send_message(chat_id=message.chat.id, text='Подписка удалена')
    return handle_settings(user, message)

def handle_subscribe(user: User, message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Группы', callback_data='subscribe_groups'),
        InlineKeyboardButton(text='Преподаватели', callback_data='subscribe_teacher'),
    )
    markup.add(
        InlineKeyboardButton(text='⬅️ Назад', callback_data='settings')
    )
    return bot.send_message(
        chat_id=message.chat.id,
        text='🆕 Раздел *Подписаться*',
        reply_markup=markup,
        parse_mode='Markdown'
    )

def handle_subscribe_groups(user: User, message: Message):
    groups = dict()
    for group in Groups.all(session):
        if not group.year in groups:
            groups[group.year] = []
        groups[group.year].append(group)
    markup = InlineKeyboardMarkup()
    for year in groups.keys():
        buttons = []
        for group in groups.get(year, []):
            buttons.append(
                InlineKeyboardButton(
                    text=group.name, callback_data=f'subscribe_groups_{group.id}'
                )
            )
        markup.add(*buttons)
    markup.add(
        InlineKeyboardButton(text='⬅️ Назад', callback_data='subscribe')
    )
    return bot.send_message(
        chat_id=message.chat.id,
        text='🆕 Раздел *Подписка по группам*',
        reply_markup=markup,
        parse_mode='Markdown'
    )

def handle_subscribe_group(user: User, message: Message, opt: Dict = None):
    group = Groups.get_by_id(session, int(opt.get('id', 0)))
    print(group)
    if group:
        # добавляем в базу
        bot.send_message(
            chat_id=message.chat.id,
            text=f'✅ Подписка на *{group.name}* успешно добавлена',
            parse_mode='Markdown'
        )
    return handle_subscribe_groups(user, message)

def handle_subscribe_teacher(user: User, message: Message):
    markup = InlineKeyboardMarkup()
    # добавить преподавателя
    markup.add(
        InlineKeyboardButton(text='⬅️ Назад', callback_data='subscribe')
    )
    return bot.send_message(
        chat_id=message.chat.id,
        text='🆕 Раздел *Подписка по преподавателям*',
        reply_markup=markup,
        parse_mode='Markdown'
    )


if __name__ == '__main__':
    print('Starting server')
    bot.infinity_polling()