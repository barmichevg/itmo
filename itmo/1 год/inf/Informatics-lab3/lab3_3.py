'''465142 % 8 = 6 => Вам необходимо поменять падежи в тексте у прилагательных, которые встречаются
несколько раз. На вход подаётся текст и порядковый номер слова, падежная форма
которого будет использована для замены.'''
import re
import json

my_json = {}
my_answers = []

def solve(num,string):
    pattern1=r'[А-я]+(?=ой|ий|ый|ая|яя|ое|ее|ые|ие|ого|его|ой|ей|ых|их|ому|ему|ой|ей|ым|им|ой|ий|ый|ую|юю|ое|ее|ого|его|ой|ей|ые|ие|ых|их|им|ым|ой|ей|ыми|ими|ом|ой|ей|ых|их)'
    roots = [i.lower() for i in re.findall(pattern1, string)]
    c=0
    root=[]
    for i in roots:
        if roots.count(i)>=2:c+=1
        if c==num:
            root=i
            pattern2 = rf'[{i[0]},{i[0].upper()}]{i[1:]}+(ой|ий|ый|ая|яя|ое|ее|ые|ие|ого|его|ой|ей|ых|их|ому|ему|ой|ей|ым|им|ой|ий|ый|ую|юю|ое|ее|ого|его|ой|ей|ые|ие|ых|их|им|ым|ой|ей|ыми|ими|ом|ой|ей|ых|их)[^А-я]'
            w_end=re.findall(pattern2, string)[num-1]
            break
    if root!=[]:
        string=re.sub(rf'[{root[0].upper()}]{root[1:]}+(ой|ий|ый|ая|яя|ое|ее|ые|ие|ого|его|ой|ей|ых|их|ому|ему|ой|ей|ым|им|ой|ий|ый|ую|юю|ое|ее|ого|его|ой|ей|ые|ие|ых|их|им|ым|ой|ей|ыми|ими|ом|ой|ей|ых|их)[^А-я]',root[0].upper()+root[1:]+w_end+' ',string)
        string=re.sub(rf'[{root[0]}]{root[1:]}+(ой|ий|ый|ая|яя|ое|ее|ые|ие|ого|его|ой|ей|ых|их|ому|ему|ой|ей|ым|им|ой|ий|ый|ую|юю|ое|ее|ого|его|ой|ей|ые|ие|ых|их|им|ым|ой|ей|ыми|ими|ом|ой|ей|ых|их)[^А-я]',root+w_end+' ',string)
    return string

inp=input('Введите строку для задания 3: ')
num = int(re.search(r'Номер[:]*\s*(\d*)',inp)[0].split(' ')[-1])
string = re.search(r'Тест[:]*\s*([^\n]*)',inp)[0].split(' ',1)[-1]
rez=solve(num,string)
my_answers.append(rez)
print('Ответ:',rez)

my_json["answers"] = my_answers
with open('result.json', 'w', encoding="utf-8") as file:
    dumped_json = json.dumps(my_json, ensure_ascii=False)
    file.write(dumped_json)