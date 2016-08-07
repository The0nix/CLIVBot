# -*- coding: utf-8 -*-
import telebot
import pickle
import datetime
import re
from collections import defaultdict
from scheduleParser import parse_schedule
from my_lib import *
from consts import *
from telebot import types
if __name__ == "__main__":
    import sys
    print( 'HELLO %s' % str(sys.argv[1]))
    import os
    import os
    port = os.environ['PORT']
    print(port)

bot = telebot.TeleBot(BOT_TOKEN)

user_actions = {}

print("----------\nSTARTED!\n----------")

@bot.message_handler(commands=['start', 'menu'])
def handle_start(message):
    """
    Shows keyboard.
    """
    debug_message(message)
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(True, row_width=2)
        itembtn1 = types.KeyboardButton(CHECK_SCHEDULE_TEXT)
        itembtn2 = types.KeyboardButton(CHECK_TASKS_TEXT)
        itembtn3 = types.KeyboardButton(ADD_TASK_TEXT)
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, START_MESSAGE_PRIVATE, reply_markup=markup)

@bot.message_handler(commands=['help'])
def handle_help(message):
    """
    Shows help.
    """
    debug_message(message)
    msg = bot.send_message(message.chat.id, HELP_MESSAGE)

@bot.message_handler(commands=['history'])
def handle_history(message):
    """
    Sends all the tasks.
    """
    debug_message(message)
    check_tasks(message, all=True)

@bot.message_handler(commands=['schedule'])
def handle_schedule(message):
    """
    Sends schedule for today and tomorrow if there is no special date provided
    otherwise shows schedule for provided date.
    """
    debug_message(message)
    text = message.text.split()
    if len(text) <= 1:
        check_schedule(message)
    elif valid_date(text[1]):
        check_schedule(message, datetime.datetime.strptime(text[1], '%d.%m.%y'),
                                datetime.datetime.strptime(text[1], '%d.%m.%y'))
    else:
        bot.send_message(message.chat.id, 'Wrong date format.')

@bot.message_handler(commands=['tasks'])
def handle_tasks(message):
    """
    Shows current tasks if there is no special date provided
    otherwise shows all tasks since provided date.
    """
    debug_message(message)
    text = message.text.split()
    if len(text) <= 1:
        check_tasks(message)
    elif valid_date(text[1]):
        check_tasks(message, since=datetime.datetime.strptime(text[1], '%d.%m.%y'))
    else:
        bot.send_message(message.chat.id, 'Wrong date format.')


@bot.message_handler(commands=['commands'])
def handle_commands(message):
    """
    Shows commands.
    """
    debug_message(message)
    bot.send_message(message.chat.id, COMMANDS)

@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    """
    Cancels current action:
    removes user's id from user_actions dictionary if it is there.
    Shows menu after cancelation.
    """
    debug_message(message)
    if message.from_user.id not in user_actions.keys():
        bot.send_message(message.chat.id, CANCEL_FAIL_TEXT)
    else:
        action = user_actions[message.from_user.id];
        del user_actions[message.from_user.id];
        bot.send_message(message.chat.id, '"{0}" canceled'.format(action))
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(True, row_width=2)
        itembtn1 = types.KeyboardButton(CHECK_SCHEDULE_TEXT)
        itembtn2 = types.KeyboardButton(CHECK_TASKS_TEXT)
        itembtn3 = types.KeyboardButton(ADD_TASK_TEXT)
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(message.chat.id, START_MESSAGE_PRIVATE, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    """
    Handles three different menu commands:
    "Check schedule", "Check hometask" and "Add hometask".
    """
    debug_message(message)
    if message.from_user.id not in user_actions.keys():
        if message.text == CHECK_SCHEDULE_TEXT:
            check_schedule(message)
        elif message.text == CHECK_TASKS_TEXT:
            check_tasks(message)
        elif message.text == ADD_TASK_TEXT:
            add_task_enter(message)
    else:
        if user_actions[message.from_user.id] == 'Task adding':
            try:
                add_task(message)
            except WrongFormatError:
                bot.send_message(message.chat.id, WRONG_FORMAT_TEXT)
            except WrongDateFormatError:
                bot.send_message(message.chat.id, WRONG_DATE_FORMAT_TEXT)
            except WrongDisciplineError:
                bot.send_message(message.chat.id, WRONG_DISCIPLINE_TEXT)

def check_tasks(message, since = datetime.datetime.today(), all = False):
    """
    Loads tasks from 'tasks.pickle' and sends them in message
    If there are no tasks sends NO_TASKS_MESSAGE.
    """
    with open('tasks.pickle', 'rb') as f:
        try:
            tasks = pickle.load(f)
        except EOFError:
            print('----------\nPickle EOF Error!\n----------')
            tasks = {}
            with open('tasks.pickle', 'wb') as f:
                pickle.dump(tasks, f)
        answer = ''
        if len(tasks) > 0:
            for disc in tasks:
                if any(date >= since for date in tasks[disc]) or all:
                    answer += '<b>{0}</b>:\n'.format(disc)
                    for date in sorted(tasks[disc]):
                        if date >= since or all:
                            answer += '\t\t\t\t\t[{0}]:\n'.format(date.strftime('%d.%m.%y'))
                            for task in tasks[disc][date]:
                                answer += '\t\t\t\t\t• {0}\n'.format(task)
        else:
            answer = NO_TASKS_MESSAGE
        if not answer:
            answer = NO_TASKS_MESSAGE
        bot.send_message(message.chat.id, answer, parse_mode='HTML')

def add_task_enter(message):
    """
    Enters into 'Task adding' state.
    """
    markup = types.ReplyKeyboardHide(selective=False)
    bot.send_message(message.chat.id, ADD_TASK_MESSAGE, reply_markup=markup)
    user_actions[message.from_user.id] = 'Task adding'

def add_task(message):
    """
    Checks if message contents proper task and if it does
    adds it in tasks.pickle.
    """
    if not re.match('.*;.*;.*', message.text): raise WrongFormatError
    data = [s.strip() for s in message.text.split(';')]
    if not valid_date(data[1]): raise WrongDateFormatError
    data[1] = datetime.datetime.strptime(data[1], '%d.%m.%y')
    if not data[0].lower() in DISCIPLINE_ALIASES.keys(): raise WrongDisciplineError
    data[0] = DISCIPLINE_ALIASES[data[0].lower()]
    with open('tasks.pickle', 'rb') as f:
        try:
            tasks = pickle.load(f)
        except EOFError:
            print('----------\nPickle EOF Error!\n----------')
            tasks = {}
            with open('tasks.pickle', 'wb') as f:
                pickle.dump(tasks, f)
        write_task(tasks, data)
    with open('tasks.pickle', 'wb') as f:
        pickle.dump(tasks, f)
    bot.send_message(message.chat.id, SUCCESSFUL_ADDING_TEXT)
    if message.from_user.id in user_actions:
        del user_actions[message.from_user.id];
    handle_start(message)

def check_schedule(message, st = datetime.datetime.today(), fin = datetime.date.today() + datetime.timedelta(days=1)):
    """
    Downloads schedule since st to fin from RUZ and
    sends it to user in nice form.
    """
    subjs = sorted(parse_schedule(st, fin),
                   key=lambda subj: (subj.date, subj.begin_lesson))
    text = ''
    dates = defaultdict(list)
    for subj in subjs:
        dates[subj.date].append(subj)
    for date in sorted(dates.keys()):
        text += '[{}]\n'.format(date.strftime('%d.%m.%Y'))
        for subj in dates[date]:
            text += '• {}–{}:{}\n\t\t\t\t{}. Aud. <b>#{}</b>\n'.format(
                subj.begin_lesson.strftime('%H:%M'),
                subj.end_lesson.strftime('%H:%M'),
                '' if subj.subgroup == SUBGROUP_BOTH else
                '\n\t\t\t\t<b>(Subgroup 1)</b>' if subj.subgroup == SUBGROUP_1 else
                '\n\t\t\t\t<b>(Subgroup 2)</b>',
                subj.discipline,
                subj.auditorium
            )
        text += '\n'
    if not text:
        text = 'No classes.'
    bot.send_message(message.chat.id, text, parse_mode='HTML')

def debug_message(message):
    """
    Prints information about message to console.
    """
    print('[{}]\n>> "{}"\n>> From "{} {}" (@{} : {}) in chat "{}" ({}). Message id: {}'.format(
        datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y %H:%M:%S'),
        message.text,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        message.from_user.id,
        message.chat.title,
        message.chat.id,
        message.message_id))

bot.polling()
