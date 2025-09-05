import pandas
from datetime import datetime, timedelta
import numpy
pandas.set_option('display.max_rows', None)
#numpy.set_printoptions(threshold=numpy.nan)

df=pandas.read_excel('data.xlsx')

x22=df.iloc[1746:2111, [0,1]]
x23=df.iloc[2111:2476, [0,1]]
x241=df.iloc[2476:2842, [0,1]]
#Удаляем данные за 29.02, чтобы количество дней было одинаковым (2024 год был високосным)
x24=x241.drop(x241.index[59])

#формируем массив, содержащий среднюю загрузку за последние 3 года
av_load=numpy.array([])
for i in range(365):
    x1=float(x22.iloc[i, 1])
    x2=float(x23.iloc[i, 1])
    x3=float(x24.iloc[i, 1])
    av=(x1+x2+x3)/3
    if av>1:
        av_load = numpy.append(av_load, 1)
    else:
        av_load = numpy.append(av_load, av)

av_load.shape=(1,365)

#назначим цены по умолчинию - цена, которую мы хотим назначить за номер в пиковые дни, когда загрузка 100%:
#Одноместный Стандарт - 3000
#Двухместный Стандарт - 3500
#Одноместный Комфорт - 3600
#Двухместный Комфорт - 4200
#Люкс - 5000
default_prices=numpy.array([[3000],[3500],[3600],[4200],[5000]])

#Сформируем прайс лист на 2025 год: цена номера в конкретный день получается умножением цены по умолчанию на процент загрузки
#Например, в Новый Год, когда ожидается загрузка = 1 цена будет 3000*1=3000, а в день, когда ожидается загрузка = 0.5 цена будет
#3000*0.5 = 1500. Перемножим матрицы default_prices и av_load

price_list=numpy.array((5, 365))
price_list=default_prices @ av_load

#Окгругляем цены
for i in range(5):
    for j in range(365):
        price_list[i][j]=round(price_list[i][j])
price_list=price_list.astype(int)

def myRound(a):
    dig=str(a)
    dig=dig[:-1]+'0'
    return int(dig)
    
for i in range(5):
    for j in range(365):
        price_list[i][j]=myRound(price_list[i][j])

#Выводим цены в эксель файл price list:
columns=[]
day1 = datetime(2025, 1, 1)
for i in range(365):
    columns.append(datetime.date(day1))
    day1=day1+timedelta(days=1)

price_list_output=pandas.DataFrame(price_list, columns=columns, index=['Одноместный Стандарт', 'Двухместный Стандарт',
                                                                       'Одноместный Комфорт', 'Двухместный Комфорт', 'Люкс'])
price_list_output.to_excel('price list.xlsx')

