import config
import xlrd
import datetime
import time
import os
import json

even_now = (int (time.strftime('%U',time.localtime())) % 2)

if os.path.isfile(config.schedule_dump):
    with open(config.schedule_dump, 'r') as base:
        schedule_dict = json.loads(base.read())
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

def day_schedule_now(group, subgroup):
    day = int(time.strftime("%w", time.localtime())) - 1
    even= int (time.strftime('%U',time.localtime())) % 2      ##test
    return schedule_dict[group][subgroup][even][config.list_of_days[day]]
