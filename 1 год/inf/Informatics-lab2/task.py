print("Введите строку:")
string=input()
sb=['r1', 'r2', 'i1', 'r3', 'i2', 'i3', 'i4']
if len(string)!=7 or bool(set(string)-{'1','0'}):
    print("Строка должна состоять из 7 цифр 0 или 1, записанных без пробелов")
    while len(string)!=7 or bool(set(string)-{'1','0'}):
        print("Введите строку снова:")
        string = input()
array=list(map(int,list(string)))
s1=(array[0] + array[2] + array[4] + array[6])%2
s2=(array[1] + array[2] + array[5] + array[6])%2
s3=(array[3] + array[4] + array[5] + array[6])%2
S=(s1,s2,s3)
if S != (0,0,0):
    num=int(''.join(map(str, S[::-1])),2)
    print("Ошибка в", sb[num-1])
    array[num-1]=1-array[num-1]
    rez=''.join(map(str, array))
    print("Правильное сообщение:", rez)
    result = sb[num-1]
else:
    print("correct")
    result = "correct"
with open('result.txt', 'w', encoding="utf-8") as file:
    file.write(result)