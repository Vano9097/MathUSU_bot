#import schedule
import config
import json
import xlrd
import format_out
import Serializing

def update_free_rooms(group_schedule):
        set_of_rooms = set()
        dict_of_rooms = dict()
        for  group in config.list_of_groups:
                for subgroup in [0,1]:
                        for week in [0,1]:
                                dict_of_rooms.setdefault(week,dict())
                                for day in config.list_of_days:
                                        dict_of_rooms[week].setdefault(day,dict())
                                        for pair_n, pair in enumerate(group_schedule[group][subgroup][week][day]):
                                                dict_of_rooms[week][day].setdefault(pair_n,set())
                                                set_of_rooms.update(set(format_out.room(pair)))
                                                dict_of_rooms[week][day][pair_n].update(set(format_out.room(pair)))
        return [set_of_rooms, dict_of_rooms]
        

def update_group_schedule():
        rez = dict()
        for group in config.list_of_groups:
                rez.setdefault(group, [[request(group, subgroup)
                        for request in [up_week_schedule_test, down_even_week_schedule_test]]
                        for subgroup  in [0,1]])
        return rez

def up_week_schedule_test(group, subgroup):
    return  {day : day_schedule_to_week(group, subgroup, day, 0) for day in config.list_of_days }
def down_even_week_schedule_test(group, subgroup):
    return  {day : day_schedule_to_week(group, subgroup, day, 1) for day in config.list_of_days }

def day_schedule_to_week(group,subgroup,day,even):
    page = int(group[3]) -1
    sheet = rb.sheet_by_index(page)
    group = config.groups_col[group] + subgroup
    rez=[]
    shift = sum(map (lambda x : config.number_of_pairs[x]*2, config.list_of_days[:config.days[day]]))
    for i in range(config.schedules_shift+shift + even ,config.schedules_shift+config.number_of_pairs[day]*2+shift ,2):
        rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    """if day < 5:
        for i in range(5+day*12 + even ,17+day*12 ,2):
            rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    else:
        for i in range(5+5*12 + even ,15+5*12 ,2):
            rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    #rb.unload_sheet(page)"""
        
    
    return rez
        
# rez [группа] [подгруппа] [верхняя = 0, нижняя = 1]
        
#print(rez['мт-102'][0][1]['понедельник'])

if __name__ == '__main__':
        rb = xlrd.open_workbook('schedule.xls',formatting_info=True)
        group_schedule = update_group_schedule()
        
        with open(config.schedule_dump, 'w') as base:
            base.write(json.dumps(group_schedule))
        
        with open(config.rooms_dump, 'w') as base:
                base.write(json.dumps(update_free_rooms(group_schedule), cls=Serializing.JSONSetEncoder))
