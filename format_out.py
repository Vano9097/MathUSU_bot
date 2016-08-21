import config

rooms = [{'614', '632', '528', '540', '628', '509', '526', '532', '513'}, {'614', '540', '628', '625', '622а', '513', '623', '602', '528', '601', '526', '612', '509', '608', '532', '605'}, {'614', '540', '625', '622а', '513', '623', '602', '632', '528', '601', '526', '612', '509', '608', '532'}, {'614', '540', '628', '625', '622а', '513', '623', '602', '528', '601', '526', '612', '509', '608', '532', '605'}, {'614', '540', '628', '625', '622а', '513', '623', '602', '632', '528', '601', '526', '612', '509', '608', '532', '605'}, {'614', '540', '628', '625', '622а', '513', '623', '602', '632', '528', '601', '526', '612', '509', '608', '532', '605'}]
pair = ['I   9:00', 'Русский язык и культура речи', ' 622', ' доц. Михайлова Ю.А.']
day = [['I   9:00', 'иностранный язык', ' 608', ' 612', ' 601', ' 605', ' 622а', ' 602', ' 623', ' 625'], ['II 10:40', 'Линейная алгебра', ' 632', ' проф. Сизый С.В.'], ['III 12:50', 'Русский язык и культура речи', ' 628', ' Ицкович Т.В.'], ['IV 14:30', 'Философия', ' 632', ' доц. Кудрявцева В.И.'], ['V 16:10', ''], ['VI 17:50', '']]

def out_free_rooms_now(rooms,pair):
    return str(pair + 1) + " пара: " + " ".join(sorted(list(rooms)) )

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

def out_lesson(pair):
    return pair_n(pair) +' ' + lesson(pair).capitalize() + ' '+ teacher(pair) +' ' + ' '.join(room(pair)) +'\n'
    

def out_day (day):
    s=''
    for pair in day:
        s+= out_lesson(pair)
    return s
def out_week(week):
    s=''
    for day in config.list_of_days:
        s+=day.capitalize() + '\n' + out_day(week[day])
    return s
