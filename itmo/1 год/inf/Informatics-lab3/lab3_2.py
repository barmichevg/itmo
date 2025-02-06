'''465142 % 6 = 4 => Анатолий выложил пост с расписанием доп. занятий по информатике, но везде
перепутал время. Поэтому нужно заменить все вхождения времени на строку (TBD).
Время – это строка вида HH:MM:SS или HH:MM, в которой HH – число от 00 до 23,
а MM и SS – число от 00 до 59.'''
import re
import json

my_json = {}
my_answers = []

def solve(string):
    pattern = r'(?<![\S])[0-1][0-9](:[0-5][0-9]){1,2}(?![\S])|(?<![\S])[2][0-3](:[0-5][0-9]){1,2}(?<![\S])'
    return re.sub(pattern, '(TBD)', string)

string=input('Введите строку для задания 2: ')
rez=solve(string)
my_answers.append(rez)
print('Ответ:',rez)

my_json["answers"] = my_answers
with open('result.json', 'w', encoding="utf-8") as file:
    dumped_json = json.dumps(my_json, ensure_ascii=False)
    file.write(dumped_json)