import config

rooms = [{'614', '632', '528', '540', '628', '509', '526', '532', '513'}, {'614', '540', '628', '625', '622а', '513', '623', '602', '528', '601', '526', '612', '509', '608', '532', '605'}, {'614', '540', '625', '622а', '513', '623', '602', '632', '528', '601', '526', '612', '509', '608', '532'}, {'614', '540', '628', '625', '622а', '513', '623', '602', '528', '601', '526', '612', '509', '608', '532', '605'}, {'614', '540', '628', '625', '622а', '513', '623', '602', '632', '528', '601', '526', '612', '509', '608', '532', '605'}, {'614', '540', '628', '625', '622а', '513', '623', '602', '632', '528', '601', '526', '612', '509', '608', '532', '605'}]

def out_free_rooms(list_rooms):
    s=""
    for pair , room in enumerate(list_rooms):
        s+= str(pair + 1) + " пара: " + " ".join(sorted(list(room)) )+ "\n"
    return s

def pair_n (pair):
    return pair[0].lstrip()
def lesson (pair):
    return pair[1].lstrip()
def teacher(pair):
    rez =pair[-1].lstrip()
    if rez.isalpha():
        return rez
    return ''

def room(pair):
    rez=[]
    try:
        for r in pair[2:]:
            i = r.lstrip()
            if int(i[0]) in [0,1,2,3,4,5,6,7,8,9]:
                rez.append(i)
    except ValueError:
        #print(i)
        return rez
    return rez

def out_day (day):
    s=''
    for pair in day:
        s+= pair_n(pair) +' ' + lesson(pair).capitalize() + ' '+ teacher(pair) +' ' + ' '.join(room(pair)) +'\n'
    return s
def out_week(week):
    s=''
    for day in config.list_of_days:
        s+=day.capitalize() + '\n' + out_day(week[day])
    return s
