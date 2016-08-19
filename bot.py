# -*- coding: utf-8 -*-
import config
import telebot
import schedule
import time
import format_out
import json
import os
from Serializing import *
import read_xls

config.list_of_groups, config.list_of_courses = read_xls.update_groups()

bot = telebot.TeleBot(config.token)

if os.path.isfile(config.users_dump):
    with open(config.users_dump, 'r') as base:
        user_dict = json.loads(base.read(), object_hook=json_as_python_User)     
else:
    user_dict = {}

    
subgroupSelect = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)  # клавиатура выбора подгруппы
subgroupSelect.add('левая', 'правая')

groupSelect = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)  # клавиатура выбора подгруппы
groupSelect.add('Моя', 'другая')

daySelect = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)  # клавиатура выбора дня
daySelect.add('понедельник' , 'вторник' ,'среда' ,'четверг' , 'пятница' ,'суббота')
hideBoard = telebot.types.ReplyKeyboardHide()  # if sent as reply_markup, will hide the keyboar


@bot.message_handler(commands=['group'])
def choice_group(message):
    msg = bot.reply_to(message, """
                Выбери свою группу,
                Пример: мт-102
                """)
    bot.register_next_step_handler(msg, add_group_step)

def add_group_step(message):
    try:
        chat_id = message.chat.id
        group = message.text.lower() 
        if  group not in config.list_of_groups:
            bot.send_message(chat_id, 'Увы, я не знаю такой группы')
            return
            
        user = User()
        user_dict[str(chat_id)] = user 
        user.group = group
        msg = bot.reply_to(message, """Выбири свою подгруппу
левая или правая
PS: если у вас нет разделения,
то выберете левую
                               """,reply_markup=subgroupSelect)
        bot.register_next_step_handler(msg, add_subgroup_step)
    except:
        bot.reply_to(message, 'oooops')

def add_subgroup_step(message):
    try:
        chat_id = message.chat.id
        sub = message.text
        user = user_dict[str(chat_id)]
        if (sub == 'правая'):
            user.subgroup = 1         

        elif (sub == 'левая'):
            user.subgroup = 0
        else:
            bot.reply_to(message, 'ops')
        bot.send_message(chat_id, 'Я знаю твою группу : ' + user.group + '\nИ подгруппу: ' +  ('левая' if user.subgroup == 0 else 'правая' ),reply_markup=hideBoard)
        with open(config.users_dump, 'w') as base:
            base.write(json.dumps(user_dict, cls=JSONUserEncoder))
            
    except BaseException  as i:
        print(i)
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['mygroup'])
def mygroup(message):
    try:
        
        chat_id = message.chat.id
        user = user_dict[str(chat_id)]
        bot.send_message(chat_id, 'Я знаю твою группу : ' + user.group + '\nИ подгруппу :' +  ('левая' if user.subgroup == 0 else 'правая' ) ,reply_markup=hideBoard)
        
    except:
        bot.reply_to(message, '''Увы я не знаю какая у тебя группа.
Воспользуйся /group и сообщи мне свою группу''')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = User()
    user_dict[str(message.chat.id)] = user
    with open(config.users_dump, 'w') as base:
            base.write(json.dumps(user_dict, cls=JSONUserEncoder))
    msg = bot.reply_to(message,  'Привет! Я Расписание Мат-Меха! подробности по /help')
@bot.message_handler(commands=['help'])
def send_help(message):
    msg = bot.send_message(message.chat.id, """

/free_rooms - узнать свободную аудиторию
/group - выбор своей группы
/mygroup - твоя текущая группа
/schedule - расписание группы на сегодня
/schedule_day - расписание группы на выбранный день
/schedule_week - расписание группы на текущую неделю
/schedule_next_week - расписание на следующую неделю
/start - приветствие
/help - помощь


""")


@bot.message_handler(commands=['schedule_day']) 
def schedule_day(message):
    try:
        chat_id = message.chat.id
        if not str(chat_id) in user_dict.keys():
            user = User()
            user_dict[str(chat_id)] = user
            with open(config.users_dump, 'w') as base:
                base.write(json.dumps(user_dict, cls=JSONUserEncoder))
        msg = bot.reply_to(message, "Какой день тебя интересует?",reply_markup=daySelect)
        bot.register_next_step_handler(msg, schedule_day_answer)
    except:
        bot.reply_to(message, 'schedule_day')
        
def schedule_day_answer(message):
    try:
        chat_id = message.chat.id
        day = message.text
        user = user_dict[str(chat_id)]
        user.request_day=day
        user.request = "False"
        update_request(str(message.chat.id))
        while user.request == "False" :
            pass
        if user.request == "Fail":
            raise BaseException
        user.request = "False"
        bot.send_message(chat_id, format_out.out_day(schedule.day_schedule(user.request_group,user.request_subgroup,user.request_day)),reply_markup=hideBoard) 
    except BaseException  as i:
        print(i, '##')
        print("schedule_day_answer")

@bot.message_handler(commands=['schedule']) 
def schedule_now(message):
    try:
        chat_id = message.chat.id
        user = user_dict[str(chat_id)]
        user.request_group = user.group
        user.request_subgroup = user.subgroup
        bot.send_message(message.chat.id, format_out.out_day(schedule.day_schedule_now(user.request_group,user.request_subgroup)),reply_markup=hideBoard)
         
    except:
        bot.send_message(chat_id, 'Воспользуйтесь /group для сохранения своей группы')
	
@bot.message_handler(commands=['schedule_week'])  ###Расписание на верхню неделю
def schedule_week(message):
    try:
        chat_id = message.chat.id
        if not str(chat_id) in user_dict.keys():
            user = User()
            user_dict[str(chat_id)] = user
            with open(config.users_dump, 'w') as base:
                base.write(json.dumps(user_dict, cls=JSONUserEncoder))
        user = user_dict[str(chat_id)]
        user.request = "False"
        update_request(str(message.chat.id))
        while user.request == "False" :
            pass
        if user.request == "Fail":
            raise BaseException
        user.request = "False"
        bot.send_message(message.chat.id, format_out.out_week(schedule.up_week_schedule(user.request_group, user.request_subgroup)),reply_markup=hideBoard)
    except BaseException  as i:
        print(i)

	
@bot.message_handler(commands=['schedule_next_week'])  ####Расписание на нижнюю неделю
def schedule_next_week(message):
    try:
        chat_id = message.chat.id
        if not str(chat_id) in user_dict.keys():
            user = User()
            user_dict[str(chat_id)] = user
            with open(config.users_dump, 'w') as base:
                base.write(json.dumps(user_dict, cls=JSONUserEncoder))
        user = user_dict[str(message.chat.id)]
        user.request = "False"
        update_request(str(message.chat.id))
        while user.request == "False" :
            pass
        if user.request == "Fail":
            raise BaseException
        user.request = "False"
        bot.send_message(message.chat.id, format_out.out_week(schedule.down_week_schedule(user.request_group, user.request_subgroup)),reply_markup=hideBoard)
    except BaseException  as i:
        print(i)
        print(type(i))
	


@bot.message_handler(commands=['free_rooms'])

def free_rooms(message):
    try:
        chat_id = message.chat.id
        if not str(chat_id) in user_dict.keys():
            user = User()
            user_dict[str(chat_id)] = user
            with open(config.users_dump, 'w') as base:
                base.write(json.dumps(user_dict, cls=JSONUserEncoder))
        msg = bot.reply_to(message, "Какой день тебя интересует?",reply_markup=daySelect)
        bot.register_next_step_handler(msg, free_rooms_answer)
    except:
        bot.reply_to(message, 'free_rooms')

def free_rooms_answer(message):
    try:
        chat_id = message.chat.id
        day = message.text
        user = user_dict[str(chat_id)]
        user.request_day=day
        even_now = (int (time.strftime('%U',time.localtime())) % 2) ####проверить
        bot.send_message(chat_id, format_out.out_free_rooms(schedule.free_room(user.request_day,even_now)), reply_markup=hideBoard) 
    except BaseException  as i:
        print(i, '##')
        print("schedule_day_answer")
	
def  update_request(chat_id):
    try:
        if not str(chat_id) in user_dict.keys():
            user = User()
            user_dict[str(chat_id)] = user
			
        user = user_dict[str(chat_id)]
        if str(chat_id) in user_dict.keys():
            msg = bot.send_message(chat_id,"Про какую группу ты хочешь узнать?",reply_markup=groupSelect)
            bot.register_next_step_handler(msg, update_request_other_group)
        else:
            msg = bot. bot.send_message(chat_id, "Про какую группу ты хочешь узнать?")
            bot.register_next_step_handler(msg, update_request_other_group)

    except BaseException  as i:
        print(i,1)
        bot.reply_to(message, 'schedule_day_my_group_step')


def update_request_other_group(message):
    try:
        chat_id = message.chat.id
        group = message.text.lower()
        user = user_dict[str(chat_id)]
        if group == "моя":
            try:
                if  user.group != None and user.subgroup !=None:
                    user.request_group = user.group
                    user.request_subgroup = user.subgroup
                    user.request = "True"
                else:
                    raise BaseException
                    #bot.send_message(chat_id, 'Воспользуйтесь /group для сохранения своей группы') ###Exception
            except BaseException  as i:
                user.request = "Fail"
                print(i, " update_request_other_group - моя")
                
                bot.send_message(chat_id, 'Воспользуйтесь /group для сохранения своей группы')
        elif group == "другая":
            msg = bot.reply_to(message, 'Напишите группу про какую вы хотите узнать')
            bot.register_next_step_handler(msg, update_request_group)
    except BaseException  as i:
        print(i, 2)
        user.request = "Fail"
        bot.reply_to(message, 'update_request_other_group')

def update_request_group(message):
    try:
        chat_id = message.chat.id
        group = message.text.lower() 
        user = user_dict[str(chat_id)]
        if  group not in config.list_of_groups:
            bot.send_message(chat_id, 'Увы, я не знаю такой группы')
            raise BaseException
             
        user.request_group = group
        msg = bot.reply_to(message, """Выбери подгруппу

 PS: если у вас нет разделения,
 то выберете левую
                               """,reply_markup=subgroupSelect)
        bot.register_next_step_handler(msg, update_request_subgroup)
    except:
        user.request = "Fail"
        print(update_request_group)
	
def update_request_subgroup(message):
    try:
        chat_id = message.chat.id
        sub = message.text
        user = user_dict[str(chat_id)]
        if (sub == 'правая'):
            user.request_subgroup = 1
            user.request = "True"
        elif (sub == 'левая'):
            user.request_subgroup = 0
            user.request = "True"
        else:
            bot.reply_to(message, 'ops')
        
    except:
        bot.reply_to(message, 'update_request_subgroup')
        user.request = "Fail"

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
	pass
	
if __name__ == '__main__':
    bot.polling(none_stop=True)
