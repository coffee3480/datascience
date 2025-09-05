import pandas as pand
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel


#Задача: найти данные по среднегодовой температуре.
#При помощи теста Стьюдента выяснить:
#действительно ли возросла температура?

#Метод расчета скользящего среднего
def RunningAverage(a):
    RunAv=[]
    for i in range(len(a)-180, len(a)):
        RunAv.append(round(sum(a[(i-21):i])/21, 2))
    return RunAv

#изъятие данных из файла
try:
    f = pand.read_csv('temp.csv')
    data=[]
    data=f
except FileNotFoundError:
    print('File not found?!?!?!')

RunAv=RunningAverage(data.Av)

print(data)


#2 выборки: первые 50 лет и последние 50 лет
data1=data.Av[0:50]
data2=data.Av[167:218]

print(len(data1))
print(len(data2))

print(data1)
print(data2)

#Использование стандартного метода для критерия Стьюдента из scipy.stats:
stat, p = ttest_rel(data2, data1)
print('Statistics=%.3f, p=%.3f' % (stat, p))

alpha = 0.05
if p > alpha:
	print('Same distributions (fail to reject H0)')
else:
	print('Different distributions (reject H0)')

#Результат: гипотеза о равенстве выборок отвергается => температура изменилась

#Построение графика
plt.plot(data.Year, data.Av)
plt.plot(data.Year[len(data.Year)-180:len(data.Year)], RunAv)
plt.show()

#Расчет t-критерия Стьюдента вручную:
#1) средние арифметические выборок (в данном случае среднее арифметическое = математическому ожиданию)

data1av=(sum(data1))/len(data1)
data2av=(sum(data2))/len(data2)

print('Avs = ',data1av, '\t', data2av)

#Дисперсии выборок:
def variance(a, av):
    summ=0
    for i in a:
        summ+=(i-av)**2
    res = summ/(len(a)-1)
    return res

data1var=variance(data1, data1av)
data2var=variance(data2, data2av)
print('variances = ', data1var, '\t', data2var)

#Стандартные отклонения:
data1sd=data1var**0.5
data2sd=data2var**0.5
print('SD\'s = ', data1sd, '\t', data2sd)

#расчет t:
a=data2av-data1av
b=(data1var/len(data1)+data2var/len(data2))**0.5

c=a/b

print('t = ',c)

#Значение t получилось 11.17, что значительно превышает табличное значение.
#Следовательно, гипотеза о равенстве выборок отвергается,
#т.е. температура действительно изменилась.












