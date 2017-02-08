from pandas import read_csv
from pyparsing import Word, Optional, alphas, nums

data = read_csv('data.csv', skiprows=7, header=None, error_bad_lines=False, warn_bad_lines=False)

final_dict = {} 
line_number = 0

# в этом цикли пробегаемся по всем строкам в data
# и выполняем определенный набор действий для каждой строки
while line_number < len(data): 
    
    # парсинг первого столбца в строке
    column_1 = data.loc[line_number].values[0]
    line = Word(alphas + '.' + '(' + ')') + '/' + Word(alphas + '(' + ')')
    full_line = line + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line) + Optional('>' + line)
    s_c = full_line.parseString(column_1).asList()
    # s_c - список, содержащий элементы первого в строке столбца
    
    # парсинг третьего столбца в строке
    column_3 = data.loc[line_number].values[2]
    line = Word(nums)
    full_line = Optional(line + '\xa0') + Optional(line + '\xa0') + Optional(line + '\xa0') + Optional(line + '\xa0') + line + ',' + line
    prices = full_line.parseString(column_3)
    # prices - список, содержащий элементы третьего в строке столбца
    
    # Запись в source_channel только нужных элементов из s_c
    # "нужные элементы" - слова, обозначающие источник и канал. "ненужные" - типа ">"
    source_channel = []
    i = 0
    while i < (len(s_c)+1)/2:
        source_channel.append(s_c[i*2])
        i = i + 1
    
    # подсчет интересующих нас элементов в строке и запись результатов в словарь
    # интересующие нас элементы - это элементы, обозначающие, что канал платный (cpm, cpc, referral)
    dict = {}
    i = 0
    number_conversion = 0
    while i < len(source_channel):
        if source_channel[i]=='cpm':
            st = source_channel[i-1] + '/' + source_channel[i]
            dict[st] = dict.setdefault(st, 0) + 1
            number_conversion = number_conversion +1
        elif source_channel[i]=='cpc':
            st = source_channel[i-1] + '/' + source_channel[i]
            dict[st] = dict.setdefault(st, 0) + 1
            number_conversion = number_conversion +1
        elif source_channel[i]=='referral':
            st = source_channel[i-1] + '/' + source_channel[i]
            dict[st] = dict.setdefault(st, 0) + 1
            number_conversion = number_conversion + 1
        i = i + 1
    # в результате получаем словарь, в котором ключи это "источник/канал",
    # а значения ключей - это то, сколько раз "источник/канал" встречается в строке
    
    # преобразование строки из третьего столбца в число
    i = 0
    prices_str = ''
    while i < ((len(prices))-1)/2:
        prices_str = prices_str + prices[i*2]
        i = i + 1
    prices_str_float = float(prices_str) +  float(prices[i*2])/100
    
    # вычисление доли заработка, приходящейся на один платный переход
    if number_conversion != 0:
        price_onepart = prices_str_float/number_conversion
    else:
        price_onepart = 0
        
    # вычисление заработка каждого платного канала и запись результата в финальный словарь
    for f in dict.keys():
        dict[f] = dict[f]*price_onepart
        if dict[f] != 0:
            final_dict[f] = final_dict.setdefault(f, 0) + dict[f]
    
    line_number = line_number + 1

#print(final_dict)
l = lambda x: x[1]
final_dict = sorted(final_dict.items(), key=l, reverse=True)

ff = open('results.txt', 'w') # запись результатов в файл
for index in final_dict:
    print(index)
    ff.write(index[0])
    ff.write(' : ')
    ff.write(str(index[1]))
    ff.write(' $ \n')
ff.close()
input('press enter')


