import pandas as pand
import numpy as np
import matplotlib.pyplot as plt




#Задача: с сайта finance.yahoo.com получить данные о стоимости акций Microsoft
#Построить график значений стоимости по времени со скользящим средним.
#Вычислить среднее и медианное значения.




#Метод поиска среднего арифметического: принимает на вход массив, выдает значение среднего арифметического
def ArithmeticAverage(a=[]):
    av=(sum(a)) / (len(a))
    return av

#Метод вычисления медианного значения: принимает на вход массив, выдает значение медианы
def Midpoint(a=[]):
    asorted=sorted(a)#Сортируем поступивший на вход массив в порядке возрастания
    #Если в массиве нечётное число элементов, то принимает центральное значение в качестве медианы
    if((len(asorted) % 2) != 0):
        midpointIndex = (len(asorted)-1)/2
        midpoint = asorted[midpointIndex]
    else: #Если в массиве чётное число элементов, то в качестве медианы берём среднее арифметическое между двумя центральными значениями.
        ind1=(len(asorted)/2)-1
        ind2=len(asorted)/2
        midpoint = (asorted[int(ind1)]+a[int(ind2)])/2
    return midpoint


#Метод формирования running average:
def RunningAverage(a):
    RunAv=[]
    for i in range(len(a)-200, len(a)):
        RunAv.append(round(sum(a[(i-21):i])/21, 2))
    return RunAv





#файл msft.csv был скачан с сайта
try:
    f = pand.read_csv('msft.csv')
    Msft=[]
    Msft=f
except FileNotFoundError:
    print('File not found?!?!?!')


    
print(Msft)


Av=ArithmeticAverage(Msft.Close)
Mid=Midpoint(Msft.Close)
RunAv = RunningAverage(Msft.Close)

print('Average = ', Av)
print('Midpoint = ', Mid)

print('Running Average = ', RunAv)




plt.plot(Msft.Date, Msft.Close)
plt.show()


plt.plot(Msft.Date, Msft.Close)
plt.plot(Msft.Date[len(Msft.Date)-200:len(Msft.Date)], RunAv)
plt.show()












