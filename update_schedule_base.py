#import schedule
import config
import json
import xlrd
import format_out
import Serializing
import read_xls

def update_free_rooms(group_schedule):
        set_of_rooms = set()
        dict_of_rooms = dict()
        for  group in list_of_groups:
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
        

        
# [группа] [подгруппа] [верхняя = 0, нижняя = 1] [день недели]


if __name__ == '__main__':
        group_schedule = read_xls.update_group_schedule()
        list_of_groups, list_of_courses = read_xls.update_groups()
        
        with open(config.schedule_dump, 'w') as base:
            base.write(json.dumps(group_schedule))
        
        with open(config.rooms_dump, 'w') as base:
                base.write(json.dumps(update_free_rooms(group_schedule), cls=Serializing.JSONSetEncoder))
