# -*- coding: utf-8 -*-
from datetime import time

schedule = 'schedule.xls'
schedules_shift = 3
token = '' #####test bot
list_of_days = ['понедельник', 'вторник','среда' ,'четверг' , 'пятница' ,'суббота']
days = {'понедельник' : 0, 'вторник' : 1,'среда' : 2,'четверг' : 3, 'пятница' : 4,'суббота' : 5}
number_of_pairs = {'понедельник' : 6, 'вторник' : 6,'среда' : 6,'четверг' : 6, 'пятница' : 6,'суббота' : 5}
users_dump = "base.json"
schedule_dump = "schedule_base.json"
rooms_dump = "rooms.json"

ends_of_pair = [time(10,30) , time(12,10),time(14,20) ,time(16,00), time(17,40),time(19,20)]
