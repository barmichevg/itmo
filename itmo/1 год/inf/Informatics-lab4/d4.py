import time
import re
import d1

start = time.perf_counter()
for i in range(100):
    json_file = [i.strip().rstrip(',').replace('"', '') for i in open('file.json', 'r', encoding='utf-8').readlines()]
    json_length = len(json_file)
    json_ind = 0


    def json_dict():
        global json_ind
        res = {}
        while json_ind < json_length:
            json_ind += 1
            if json_file[json_ind] == '}':
                return res
            key, value = json_file[json_ind].split(': ')
            if value == '[':
                res[key] = json_list()
            elif value == '{':
                res[key] = json_dict()
            else:
                res[key] = value


    def json_list():
        global json_ind
        res = []
        while json_ind < json_length:
            json_ind += 1
            if json_file[json_ind] == '[':
                res.append(json_list())
            elif json_file[json_ind] == ']':
                return res
            else:
                res.append(json_file[json_ind])


    xml_file = open('file.xml', 'w', encoding='utf-8')
    xml_tab = 1


    def xml_dict(dictionary):
        global xml_tab
        for key, value in dictionary.items():
            if type(value) is str:
                xml_file.write('\t' * xml_tab + f'<{key}>{value}</{key}>' + '\n')
            elif type(value) is dict:
                xml_file.write('\t' * xml_tab + f'<{key}>' + '\n')
                xml_tab += 1
                xml_dict(value)
                xml_tab -= 1
                xml_file.write('\t' * xml_tab + f'</{key}>' + '\n')
            else:
                xml_list(key, value)


    def xml_list(name, array):
        global xml_tab
        for item in array:
            xml_file.write('\t' * xml_tab + f'<{name}>{item}</{name}>' + '\n')


    xml_file.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n' + '<root>' + '\n')
    xml_dict(json_dict())
    xml_file.write('</root>')
end = time.perf_counter()
print(f"Обязательное: {end - start}")

start = time.perf_counter()
for i in range(100):
    d1.start()
end = time.perf_counter()
print(f"доп 1: {end - start}")

start = time.perf_counter()
for i in range(100):
    json_file = open('file.json', 'r', encoding='utf-8').readlines()
json_file = [re.sub(r',?\n$', '', i) for i in json_file]
json_file = [re.sub(r'^\s*', '', i) for i in json_file]
json_length = len(json_file)
json_ind = 0

def json_dict():
    global json_ind
    res = {}
    while json_ind < json_length:
        json_ind += 1
        if re.search(r'}$', json_file[json_ind]):
            return res
        line = re.search(r'"(.*)": (\{|\[|"(.*)")', json_file[json_ind])
        key, value = line.group(1), line.group(2)
        if value == '[':
            res[key] = json_list()
        elif value == '{':
            res[key] = json_dict()
        else:
            res[key] = line.group(3)

def json_list():
    global json_ind
    res = []
    while json_ind < json_length:
        json_ind += 1
        search = re.search(r'.$', json_file[json_ind]).group(0)
        if search == '[':
            res.append(json_list())
        elif search == ']':
            return res
        else:
            res.append(json_file[json_ind])

xml_file = open('file_d2.xml', 'w', encoding='utf-8')
xml_tab = 1

def xml_dict(dictionary):
    global xml_tab
    for key, value in dictionary.items():
        if type(value) is str:
            xml_file.write('\t' * xml_tab + f'<{key}>{value}</{key}>' + '\n')
        elif type(value) is dict:
            xml_file.write('\t' * xml_tab + f'<{key}>' + '\n')
            xml_tab += 1
            xml_dict(value)
            xml_tab -= 1
            xml_file.write('\t' * xml_tab + f'</{key}>' + '\n')
        else:
            xml_list(key, value)

def xml_list(name, array):
    global xml_tab
    for item in array:
        xml_file.write('\t' * xml_tab + f'<{name}>{item}</{name}>' + '\n')

xml_file.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n' + '<root>' + '\n')
xml_dict(json_dict())
xml_file.write('</root>')
end = time.perf_counter()
print(f"доп 2: {end - start}")

start = time.perf_counter()
for i in range(100):
    json_file = open('file.json', 'r', encoding='utf-8').read()
    json_length = len(json_file)
    json_ind = 0


    def json_parce():
        global json_ind
        res = None
        while json_ind < json_length:
            if json_file[json_ind] in [' ', '\t', ':', ',', '\n']:
                json_ind += 1
            elif json_file[json_ind] in '1234567890':
                res = json_num()
            elif json_file[json_ind] == '"':
                res = json_string()
            elif json_file[json_ind] == '[':
                res = json_list()
            elif json_file[json_ind] == '{':
                res = json_dict()
            else:
                res = json_literal()
        return res


    def json_num():
        global json_ind
        res = ''
        while (json_ind < json_length) and (json_file[json_ind] in '1234567890-eE.'):
            res += json_file[json_ind]
            json_ind += 1
        res = re.sub(r'\.0*$', '', str(float(res)))
        return float(res) if '.' in res else int(res)


    def json_string():
        global json_ind
        res = ''
        while (json_ind < json_length) and not re.search(r'".*?[^\\]"', res):
            res += json_file[json_ind]
            json_ind += 1
        return xml_correct(res[1:-1])


    def json_literal():
        global json_ind
        if json_file[json_ind] == 'n':
            res = 'null'
            json_ind += 4
        elif json_file[json_ind] == 't':
            res = 'true'
            json_ind += 4
        else:
            res = 'false'
            json_ind += 5
        return res


    def json_dict():
        global json_ind
        json_ind += 1
        res = {}
        key = ''
        while (json_ind < json_length) and (json_file[json_ind] != '}'):
            if json_file[json_ind] in [' ', '\t', ':', ',', '\n']:
                json_ind += 1
            elif json_file[json_ind] == '"' and not key:
                key = json_string()
            elif json_file[json_ind] in '1234567890' and key:
                res[key] = json_num()
                key = ''
            elif json_file[json_ind] == '"' and key:
                res[key] = json_string()
                key = ''
            elif json_file[json_ind] == '[' and key:
                res[key] = json_list()
                key = ''
            elif json_file[json_ind] == '{' and key:
                res[key] = json_dict()
                key = ''
            else:
                res[key] = json_literal()
                key = ''
        json_ind += 1
        return res


    def json_list():
        global json_ind
        json_ind += 1
        res = []
        while (json_ind < json_length) and (json_file[json_ind] != ']'):
            if json_file[json_ind] in [' ', '\t', ':', ',', '\n']:
                json_ind += 1
            elif json_file[json_ind] in '1234567890':
                res.append(json_num())
            elif json_file[json_ind] == '"':
                res.append(json_num())
            elif json_file[json_ind] == '[':
                res.append(json_list())
            elif json_file[json_ind] == '{':
                res.append(json_dict())
            else:
                res.append(json_literal())
        json_ind += 1
        return res


    xml_replace = [('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ("'", '&apos;'), (r'\"', '&quot;')]
    xml_file = open('file_d3.xml', 'w', encoding='utf-8')
    xml_tab = 1


    def xml_correct(line):
        for i, j in xml_replace:
            line = line.replace(i, j)
        return line


    def xml_parce(json_input):
        if json_input == 'null':
            xml_file.write('\t' * xml_tab + '<item/>' + '\n')
        elif json_input in ['true', 'false']:
            xml_file.write('\t' * xml_tab + f'<item available="{json_input}"/>' + '\n')
        elif type(json_input) is str:
            xml_file.write('\t' * xml_tab + json_input + '\n')
        elif type(json_input) is list:
            xml_list('item', json_input)
        else:
            xml_dict(json_input)


    def xml_dict(dictionary):
        global xml_tab
        for key, value in dictionary.items():
            if value == 'null':
                xml_file.write('\t' * xml_tab + f'<{key}/>' + '\n')
            elif value in ['true', 'false']:
                xml_file.write('\t' * xml_tab + f'<{key} available="{value}"/>' + '\n')
            elif type(value) is list:
                xml_list(key, value)
            elif type(value) is dict:
                xml_file.write('\t' * xml_tab + f'<{key}>' + '\n')
                xml_tab += 1
                xml_dict(value)
                xml_tab -= 1
                xml_file.write('\t' * xml_tab + f'</{key}>' + '\n')
            else:
                xml_file.write('\t' * xml_tab + f'<{key}>{value}</{key}>' + '\n')


    def xml_list(name, array):
        global xml_tab
        for item in array:
            if item == 'null':
                xml_file.write('\t' * xml_tab + f'<{name}/>' + '\n')
            elif item in ['true', 'false']:
                xml_file.write('\t' * xml_tab + f'<{name} available="{item}"/>' + '\n')
            elif type(item) is list:
                raise Exception('В XML список-блок не может содержать дочерних список-блоков')
            elif type(item) is dict:
                xml_file.write('\t' * xml_tab + f'<{name}>' + '\n')
                xml_tab += 1
                xml_dict(item)
                xml_tab -= 1
                xml_file.write('\t' * xml_tab + f'</{name}>' + '\n')
            else:
                xml_file.write('\t' * xml_tab + f'<{name}>{item}</{name}>' + '\n')


    xml_file.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n' + '<root>' + '\n')
    xml_parce(json_parce())
    xml_file.write('</root>')
end = time.perf_counter()
print(f"доп 3: {end - start}")