# -*- coding: utf-8 -*-
schedule = 'schedule.xls'
schedules_shift = 5
token = ''
groups_col = { 'мт-101' : 2, 'мт-102' : 4}#groups_col = { 'мт-101' : 2, 'мт-102' : 4,'мт-201' : 2, 'мт-202' : 4 }
list_of_groups = [ 'мт-101','мт-102']#list_of_groups = [ 'мт-101','мт-102','мт-201', 'мт-202']
list_of_days = ['понедельник', 'вторник','среда' ,'четверг' , 'пятница' ,'суббота']
days = {'понедельник' : 0, 'вторник' : 1,'среда' : 2,'четверг' : 3, 'пятница' : 4,'суббота' : 5}
number_of_pairs = {'понедельник' : 6, 'вторник' : 6,'среда' : 6,'четверг' : 6, 'пятница' : 6,'суббота' : 5}
users_dump = "base.json"
schedule_dump = "schedule_base.json"
rooms_dump = "rooms.json"