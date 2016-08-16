# -*- coding: utf-8 -*-
import config
import token
import telebot
import schedule
import time
import format_out
import json
import os
from Serializing import *

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
        bot.send_message(chat_id, 'Я знаю твою группу : ' + user.group + '\n И подгруппу:' +  ('левая' if user.subgroup == 0 else 'правая' ))
        with open(config.users_dump, 'w') as base:
          #  base.write(json.dumps(user_dict))
            base.write(json.dumps(user_dict, cls=JSONUserEncoder))
            
    except BaseException  as i:
        print(i)
        bot.reply_to(message, 'oooops')

@bot.message_handler(commands=['mygroup'])
def mygroup(message):
    try:
        
        chat_id = message.chat.id
        user = user_dict[str(chat_id)]
        bot.send_message(chat_id, 'Я знаю твою группу : ' + user.group + '\n И подгруппу:' +  ('левая' if user.subgroup == 0 else 'правая' ) )
        
    except:
        bot.reply_to(message, '''Увы я не знаю какая у тебя группа.
Воспользуйся /group и сообщи мне свою группу''')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = User()
    user_dict[str(message.chat.id)] = user 
    msg = bot.reply_to(message,  'Привет! Я Расписание Мат-Меха! подробности по /help')
@bot.message_handler(commands=['help'])
def send_help(message):
    msg = bot.send_message(message.chat.id, """
/start - приветствие
/group - выбор своей группы
/mygroup - твоя текущая группа
/schedule - расписание группы на сегодня
/schedule_day - расписание группы на следующий [день недели]
/schedule_week - расписание группы на текущую неделю
/schedule_next_week - расписание на следующую неделю
/help - помощь


""")

def schedule_day_group_request(message):
    try:
        chat_id = message.chat.id
        group = message.text.lower()
        user = user_dict[str(chat_id)]
        if group == "моя":
            try:
                user.request_group = user.group
                user.request_subgroup = user.subgroup
                bot.send_message(chat_id, format_out.out_day(schedule.day_schedule(user.request_group,user.request_subgroup,user.request_day))) 
            except:
                bot.send_message(chat_id, 'Воспользуйтесь /group для сохранения своей группы')
        elif group == "другая":
            
            msg = bot.reply_to(message, """Выбири группу""")
            bot.register_next_step_handler(msg, schedule_day_group_step)
        
    except BaseException  as i:
        print(i)
        bot.reply_to(message, 'choice_group_request')

def schedule_day_group_step(message):
    try:
        chat_id = message.chat.id
        group = message.text.lower() 
        user = user_dict[str(chat_id)]
        if  group not in config.list_of_groups:
            bot.send_message(chat_id, 'Увы, я не знаю такой группы')
            return
             
        user.request_group = group
        msg = bot.reply_to(message, """Выбири свою подгруппу
левая или правая
PS: если у вас нет разделения,
то выберете левую
                               """,reply_markup=subgroupSelect)
        bot.register_next_step_handler(msg, schedule_day_choice_subgroup)
    except:
        bot.reply_to(message, 'oooops')
		
def schedule_day_choice_subgroup(message):
    try:
        chat_id = message.chat.id
        sub = message.text
        user = user_dict[str(chat_id)]
        if (sub == 'правая'):
            user.request_subgroup = 1
            bot.send_message(chat_id, format_out.out_day(schedule.day_schedule(user.request_group,user.request_subgroup,user.request_day))) 
            #user.request_user_group=user.request_group+'-'+user.request_subgroup  #костыль, нужно убрать

        elif (sub == 'левая'):
            user.request_subgroup = 0
            bot.send_message(chat_id, format_out.out_day(schedule.day_schedule(user.request_group,user.request_subgroup,user.request_day))) 
            #user.request_user_group=user.request_group+'-'+user.request_subgroup  #костыль, нужно убрать
        else:
            bot.reply_to(message, 'ops')
    except:
        bot.reply_to(message, 'schedule_day_choice_subgroup')

    

@bot.message_handler(commands=['schedule_day']) 
def schedule_day(message):
    try:
        chat_id = message.chat.id
        msg = bot.reply_to(message, "Какой день тебя интересует?",reply_markup=daySelect)
        bot.register_next_step_handler(msg, schedule_day_my_group_step)
    except:
        bot.reply_to(message, 'schedule_day')


def  schedule_day_my_group_step(message):
    try:
        chat_id = message.chat.id
        day = message.text
        user = user_dict[str(chat_id)]
        user.request_day=day
        if chat_id in user_dict.keys():
            msg = bot.reply_to(message, "Про какую группу ты хочешь узнать?",reply_markup=groupSelect)
            bot.register_next_step_handler(msg, schedule_day_group_request)
        else:
            msg = bot.reply_to(message, "Про какую группу ты хочешь узнать?")
            bot.register_next_step_handler(msg, schedule_day_group_request)
        
        #time.sleep(100)
        #print(6)
        #bot.send_message(chat_id, format_out.out_day(schedule.day_schedule(user.request_group,user.request_day)))
    except BaseException  as i:
        print(i)
        bot.reply_to(message, 'schedule_day_my_group_step')

@bot.message_handler(commands=['schedule']) 
def schedule_now(message):
    try:
        chat_id = message.chat.id
        user = user_dict[str(chat_id)]
        user.request_group = user.group
        user.request_subgroup = user.subgroup
        bot.send_message(message.chat.id, format_out.out_day(schedule.day_schedule_now(user.request_group,user.request_subgroup)))
         
    except:
        bot.send_message(chat_id, 'Воспользуйтесь /group для сохранения своей группы')
	
@bot.message_handler(commands=['schedule_week']) #group
def schedule_week(message):
    try:            
        update_request(str(message.chat.id))
        user = user_dict[str(message.chat.id)]
        #print(user.request_group, user.request_subgroup)
        bot.send_message(message.chat.id, format_out.out_week(schedule.week_schedule(user.request_group, user.request_subgroup)))
    except BaseException  as i:
        print(i)
   
            
        #send_help(message)
	
@bot.message_handler(commands=['schedule_next_week']) #group
def schedule_next_week(message):
    try:            
        a = update_request(str(message.chat.id))
        #print(type(a),a)
        user = user_dict[str(message.chat.id)]
        #print(user.request_group, user.request_subgroup)
        bot.send_message(message.chat.id, format_out.out_week(schedule.next_week_schedule(user.request_group, user.request_subgroup)))
    except BaseException  as i:
        print(i)
        print(type(i))
        #send_help(message)
	
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    #bot.send_message(message.chat.id, message.text)
	pass

	
def  update_request(chat_id):
    try:
        if not chat_id in user_dict.keys():
            user = User()
            user_dict[str(chat_id)] = user
			
        user = user_dict[str(chat_id)]
        if chat_id in user_dict.keys():
            msg = bot.send_message(chat_id,"Про какую группу ты хочешь узнать?",reply_markup=groupSelect)
            bot.register_next_step_handler(msg, update_request_other_group)
        else:
            msg = bot. bot.send_message(chat_id, "Про какую группу ты хочешь узнать?")
            bot.register_next_step_handler(msg, update_request_other_group)
        
        #time.sleep(100)
        #print(6)
        #bot.send_message(chat_id, format_out.out_day(schedule.day_schedule(user.request_group,user.request_day)))
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
                user.request_group = user.group
                user.request_subgroup = user.subgroup
            except:
                bot.send_message(chat_id, 'Воспользуйтесь /group для сохранения своей группы')
        elif group == "другая":
            msg = bot.reply_to(message, 'Напишите группу про какую вы хотите узнать')
            bot.register_next_step_handler(msg, update_request_group)
    except BaseException  as i:
        print(i, 2)
        bot.reply_to(message, 'update_request_other_group')

def update_request_group(message):
    try:
        chat_id = message.chat.id
        group = message.text.lower() 
        user = user_dict[str(chat_id)]
        if  group not in config.list_of_groups:
            bot.send_message(chat_id, 'Увы, я не знаю такой группы')
            return
             
        user.request_group = group
        msg = bot.reply_to(message, """Выбери подгруппу

 PS: если у вас нет разделения,
 то выберете левую
                               """,reply_markup=subgroupSelect)
        bot.register_next_step_handler(msg, update_request_subgroup)
    except:
        bot.reply_to(message, 'oooops')
	
def update_request_subgroup(message):
    try:
        chat_id = message.chat.id
        sub = message.text
        user = user_dict[str(chat_id)]
        if (sub == 'правая'):
            user.request_subgroup = 1
            
        elif (sub == 'левая'):
            user.request_subgroup = 0
         
        else:
            bot.reply_to(message, 'ops')
        
    except:
        bot.reply_to(message, 'update_request_subgroup')
	
if __name__ == '__main__':
    bot.polling(none_stop=True)
