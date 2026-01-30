'''465142 % 6 = 4 => Глаза: =
465142 % 4 = 2 => Рот: -{
465142 % 8 = 6 => Нос: O
Смайлик: =-{O'''
import re
import json

my_json = {}
my_answers = []

def solve(string):
    pattern=r'=-{O'
    return len(re.findall(pattern, string))

string=input('Введите строку для задания 1: ')
rez=solve(string)
my_answers.append(string)
my_answers.append(rez)
print('Ответ:',rez)

my_json["answers"] = my_answers
with open('result.json', 'w', encoding="utf-8") as file:
    dumped_json = json.dumps(my_json, ensure_ascii=False)
    file.write(dumped_json)