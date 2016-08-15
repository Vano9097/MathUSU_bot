day =[['I   9:00', 'иностранный язык', '608', ' 612', ' 601', ' 605', ' 622а', ' 602', ' 623', ' 625'], ['II 10:40', 'Линейная алгебра', ' 632', ' проф. Сизый С.В.'], ['III 12:50', 'Русский язык и культура речи', ' 628', ' Ицкович Т.В.'], ['IV 14:30', 'Философия', ' 632', ' доц. Кудрявцева В.И.'], ['V 16:10', ''], ['VI 17:50', '']]
week =[[['I   9:00', 'иностранный язык 608', ' 612', ' 601', ' 605', ' 622а', ' 602', ' 623', ' 625'], ['II 10:40', 'Линейная алгебра', ' 632', ' проф. Сизый С.В.'], ['III 12:50', 'Русский язык и культура речи', ' 628', ' Ицкович Т.В.'], ['IV 14:30', 'Философия', ' 632', ' доц. Кудрявцева В.И.'], ['V 16:10', ''], ['VI 17:50', '']], [['I   9:00', ''], ['II 10:40', 'ПРИКЛАДНАЯ ФИЗИЧЕСКАЯ КУЛЬТУРА с 10:00'], ['III 12:50', 'Аа', ' 526', ' Смирнова Е.А.'], ['IV 14:30', 'Математический анализ', ' 532', ' проф. Антонов Н.Ю.'], ['V 16:10', ''], ['VI 17:50', '']], [['I   9:00', 'Математический анализ', ' 532', ' проф. Антонов Н.Ю.'], ['II 10:40', 'ин яз 608', ' 612', ' 601', ' 614', ' 622а', ' 602', '  623', ' 625'], ['III 12:50', 'М ан', ' 605', ' Бояршинов'], ['IV 14:30', ''], ['V 16:10', ''], ['VI 17:50', '']], [['I   9:00', 'Лин алгебра', ' 605', ' доц. Финогенова О.Б.'], ['II 10:40', 'АА', ' 623', ' Смирнова Е.А.'], ['III 12:50', 'М ан', ' 623', ' Бояршинов'], ['IV 14:30', ''], ['V 16:10', ''], ['VI 17:50', '']], [['I   9:00', ''], ['II 10:40', 'ПРИКЛАДНАЯ ФИЗИЧЕСКАЯ КУЛЬТУРА с 10:00'], ['III 12:50', 'Алгоритмический анализ', ' 509', ' доц. Лахтин А.С.'], ['IV 14:30', ''], ['V 16:10', ''], ['VI 17:50', '']], [['I   9:00', 'Лин алгебра', ' 605', ' доц. Финогенова О.Б.'], ['II 10:40', 'Линейная алгебра', ' 632', ' проф. Сизый С.В.'], ['III 12:50', ''], ['IV 14:30', ''], ['V 16:10', '']]]
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
        s+= pair_n(pair) +' ' + lesson(pair) + ' '+ teacher(pair) +' ' + ' '.join(room(pair)) +'\n'
    return s
def out_week(week):
    s=''
    for w, day in zip(["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"], week):
        s+=w + '\n' + out_day(day)
    return s
