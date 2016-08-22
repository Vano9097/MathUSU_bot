import config
import xlrd
import datetime
import time
import os
import json
import Serializing
even_now = (int (time.strftime('%U',time.localtime())) % 2)

if os.path.isfile(config.schedule_dump):
    with open(config.schedule_dump, 'r') as base:
        schedule_dict = json.loads(base.read())
else:
    print("update schedule base fail")
    raise BaseException("update schedule base fail")

if os.path.isfile(config.rooms_dump):
    with open(config.rooms_dump, 'r') as base:
        set_of_rooms, dict_of_rooms = json.loads(base.read(), object_hook=Serializing.json_as_python_set)
         
else:
    print("update schedule base fail")
    raise BaseException("update schedule base fail")

def up_week_schedule(group, subgroup):
    return  schedule_dict[group][subgroup][0]

def down_week_schedule(group, subgroup):
    return  schedule_dict[group][subgroup][1]

def day_schedule(group, subgroup, day):
    config.days[day]
    day_now = int(time.strftime("%w", time.localtime())) - 1
    if  config.days[day] > day_now:                                                                              ##test
        even = (int (time.strftime('%U',time.localtime())) % 2)
    else:
        even = (int (time.strftime('%U',time.localtime()))+ 1)  % 2
        
    return schedule_dict[group][subgroup][even][day]

def pair_schedule_now(group, subgroup,pair):
    try:
        
        day = int(time.strftime("%w", time.localtime())) - 1
        if day == -1: ##воскресенье 
            day = 0
        even= int (time.strftime('%U',time.localtime())) % 2      ##test
        return schedule_dict[group][subgroup][even][config.list_of_days[day]][pair]
    except IndexError:
        return schedule_dict[group][subgroup][even][config.list_of_days[day]][pair - 1]
        
def day_schedule_now(group, subgroup):
    day = int(time.strftime("%w", time.localtime())) - 1
    if day == -1: ##воскресенье 
        day = 0
    even= int (time.strftime('%U',time.localtime())) % 2      ##test
    return schedule_dict[group][subgroup][even][config.list_of_days[day]]

def free_room_now(week,pair):
    day = int(time.strftime("%w", time.localtime())) - 1
    if day == -1: ##воскресенье 
        day = 0
    return set_of_rooms.difference(dict_of_rooms[str(week)][config.list_of_days[day]][str(pair)]) 

def free_room(day,week):
    return [set_of_rooms.difference(dict_of_rooms[str(week)][day][str(pair_n)]) for pair_n in range(config.number_of_pairs[day])]
