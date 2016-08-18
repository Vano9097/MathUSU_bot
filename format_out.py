import config

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
