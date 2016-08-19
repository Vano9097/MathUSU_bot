import xlrd
import config
rb = xlrd.open_workbook(config.schedule,formatting_info=True)

#page = 0
#sheet = rb.sheet_by_index(page)
def update_groups():
    list_of_groups = []
    list_of_courses = []
    for sheet in [ rb.sheet_by_index(i) for i in range(rb.nsheets)]:
        groups_col = {}
        for i in range(sheet.ncols):
            if  sheet.cell_value(1,i) != '':
                groups_col.setdefault(sheet.cell_value(1,i).lower() , i)
                list_of_groups.append(sheet.cell_value(1,i).lower() )
        list_of_courses.append(groups_col)
    return list_of_groups , list_of_courses

list_of_groups, list_of_courses = update_groups()

def update_group_schedule():
    rez = dict()
    for page in  range(len(list_of_courses)):
        sheet = rb.sheet_by_index(page)
        for group in list_of_courses[page]:
            rez.setdefault(group, [[request(group, subgroup,page)
            for request in [up_week_schedule_test, down_even_week_schedule_test]]
            for subgroup  in [0,1]])
    return rez
def up_week_schedule_test(group, subgroup,page):
    return  {day : day_schedule_to_week(group, subgroup, day, 0,page) for day in config.list_of_days }
def down_even_week_schedule_test(group, subgroup,page):
    return  {day : day_schedule_to_week(group, subgroup, day, 1,page) for day in config.list_of_days }

def day_schedule_to_week(group,subgroup,day,even,page):
    list_of_groups, list_of_courses = update_groups()
    sheet = rb.sheet_by_index(page)
    #print(group, sheet)
    group = list_of_courses[page][group] + subgroup
    rez=[]
    shift = sum(map (lambda x : config.number_of_pairs[x]*2, config.list_of_days[:config.days[day]]))
    for i in range(config.schedules_shift+shift + even ,config.schedules_shift+config.number_of_pairs[day]*2+shift ,2):
        rez.append([unmergedValue(i,1,sheet)] + unmergedValue(i,group,sheet).split(',')) ###del номер пары
        if unmergedValue(i,group,sheet) != "" :
            #print(sheet.cell_value(i,group))
            pass
    return rez

def unmergedValue(rowx,colx,thesheet):
    for crange in thesheet.merged_cells:
        rlo, rhi, clo, chi = crange
        if rowx in range(rlo, rhi):
            if colx in range(clo, chi):
                return thesheet.cell_value(rlo,clo)
    #if you reached this point, it's not in any merged cells
    return thesheet.cell_value(rowx,colx)

