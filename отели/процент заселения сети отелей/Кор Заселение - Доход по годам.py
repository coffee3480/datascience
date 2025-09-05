import pandas
from numpy.linalg import qr, inv
from sklearn.linear_model import LinearRegression
import numpy
import matplotlib.pyplot as plt
from scipy.stats import t
from math import sqrt

df=pandas.read_excel('data.xlsx')
data=df.to_numpy()

x_17=numpy.array([])
x_18=numpy.array([])
x_19=numpy.array([])
x_20=numpy.array([])
x_21=numpy.array([])
x_22=numpy.array([])
x_23=numpy.array([])
x_24=numpy.array([])
x_25=numpy.array([])
year=2017
for j in (x_17, x_18, x_19, x_20, x_21, x_22, x_23, x_24, x_25):
    if j is x_17:
        i1=0
        i2=365
    elif j is x_18:
        i1=365
        i2=730
    elif j is x_19:
        i1=730
        i2=1015
    elif j is x_20:
        i1=1015
        i2=1381
    elif j is x_21:
        i1=1381
        i2=1746
    elif j is x_22:
        i1=1746
        i2=2111
    elif j is x_23:
        i1=2111
        i2=2476
    elif j is x_24:
        i1=2476
        i2=2842
    elif j is x_25:
        i1=2842
        i2=3040
    for i in range(i1, i2):
        j=numpy.append(j, data[i][1])
    print('Средний спрос за', year, ' : ', round(numpy.mean(j),2))
    year+=1
    
#2142-2475 : 2023, 2476-2841 : 2024, 2842-3039 : 2025
x23=[]
y23=[]
z23=[]
x24=[]
y24=[]
z24=[]
x25=[]
y25=[]
z25=[]

for i in range(2142, 2476):
    x23.append(data[i][1])
    y23.append(round(data[i][8]))
    z23.append(round(data[i][11]))

for i in range(2476, 2842):
    x24.append(data[i][1])
    y24.append(round(data[i][8]))
    z24.append(round(data[i][11]))

for i in range(2842, 3040):
    x25.append(data[i][1])
    y25.append(round(data[i][8]))
    z25.append(round(data[i][11]))
    
year=2023
for j in ((x23, y23, z23), (x24, y24, z24), (x25, y25, z25)):
    print(year,':')
    x1=numpy.vstack([j[0], numpy.ones(len(j[0]))]).transpose()
    z1=numpy.vstack([j[2], numpy.ones(len(j[2]))]).transpose()
    Q1, R1 = qr(x1)
    Q2, R2 = qr(z1)
    bxy=inv(R1) @ Q1.transpose() @ j[1]
    bxz=inv(R1) @ Q1.transpose() @ j[2]
    bzy=inv(R2) @ Q2.transpose() @ j[1]
    k=bxy[0]
    b=bxy[1]
    kzy=bzy[0]
    bzy=bzy[1]
    kxz=bxz[0]
    bxz=bxz[1]
    X=pandas.DataFrame(j[0])
    Y=pandas.DataFrame(j[1])
    Z=pandas.DataFrame(j[2])
    xy=[]
    zy=[]
    xz=[]
    for i in range(len(j[0])):
        xy.append([j[0][i], j[1][i]])
        xz.append([j[0][i], j[2][i]])
        zy.append([j[1][i], j[2][i]])
    XY=pandas.DataFrame(xy)
    XZ=pandas.DataFrame(xz)
    ZY=pandas.DataFrame(zy)
    r=XY.corr(method='pearson')
    r=r[0][1]
    print('Коэффициент корреляции уровня заселения и дохода: ', round(r,2))
    r=ZY.corr(method='pearson')
    r=r[0][1]
    print('Коэффициент корреляции цены номера и дохода: ', round(r,2))
    r=XZ.corr(method='pearson')
    r=r[0][1]
    print('Коэффициент корреляции уровня заселения и цены номера: ', round(r,2))
    
    plt.scatter(X, Y)
    plt.plot(X, k*X+b, color='orange', label='%заселения и доход')
    plt.xlabel('Уровень заселения номерного фонда, %')
    plt.ylabel('Доход, млн. рублей')
    plt.title(str(year))
    plt.show()
    plt.scatter(Z,Y)
    plt.plot(Z, kzy*Z+bzy, color='orange')
    plt.xlabel('Цена номера за день, рублей')
    plt.ylabel('Доход, млн. рублей')
    plt.title(str(year))
    plt.show()
    plt.scatter(X,Z)
    plt.plot(X, kxz*X+bxz, color='orange')
    plt.xlabel('Уровень заселения номерного фонда, %')
    plt.ylabel('Цена номера за день, рублей')
    plt.title(str(year))
    plt.show()

    year+=1



