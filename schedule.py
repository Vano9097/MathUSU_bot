import config
import xlrd
import datetime
import time

even_now = (int (time.strftime('%U',time.localtime())) % 2)

rb = xlrd.open_workbook('schedule.xls',formatting_info=True)


def week_schedule(group, subgroup):
    return  [day_schedule_to_week(group, subgroup, day,int (time.strftime('%U',time.localtime())) % 2) for day in config.list_of_days ]

def next_week_schedule(group, subgroup):
    return  [day_schedule_to_week(group, subgroup, day,  (int (time.strftime('%U',time.localtime())) + 1)  % 2   ) for day in config.list_of_days ]


    
def day_schedule_to_week(group,subgroup,day,even):
    page = int(group[3]) -1
    sheet = rb.sheet_by_index(page)
    group = config.groups_col[group] + subgroup
    day=config.days[day]
    rez=[]
    if day < 5:
        for i in range(5+day*12 + even ,17+day*12 ,2):
            rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    else:
        for i in range(5+5*12 + even ,15+5*12 ,2):
            rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    #rb.unload_sheet(page)
    return rez


def day_schedule(group, subgroup, day):
    page = int(group[3]) -1
    sheet = rb.sheet_by_index(page)
    group = config.groups_col[group] + subgroup
    day=config.days[day]
    day_now = int(time.strftime("%w", time.localtime())) - 1
    if  day > day_now:
        even = (int (time.strftime('%U',time.localtime())) % 2)
    else:
        even = (int (time.strftime('%U',time.localtime()))+ 1)  % 2
        
    rez=[]
    if day < 5:
        for i in range(5+day*12 + even ,17+day*12 ,2):
            rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    else:
        for i in range(5+5*12 + even ,15+5*12 ,2):
            rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    #rb.unload_sheet(page)
    return rez



def day_schedule_now(group, subgroup):
    page = int(group[3]) -1
    sheet = rb.sheet_by_index(page)
    group = config.groups_col[group] + subgroup
    day = int(time.strftime("%w", time.localtime())) - 1
    even= int (time.strftime('%U',time.localtime())) % 2    
    rez=[]
    if day < 5:
        for i in range(5+day*12 + even ,17+day*12 ,2):
            rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    else:
        for i in range(5+5*12 + even ,15+5*12 ,2):
            rez.append([sheet.cell_value(i,1)] + sheet.cell_value(i,group).split(','))
    #rb.unload_sheet(page)

    return rez
