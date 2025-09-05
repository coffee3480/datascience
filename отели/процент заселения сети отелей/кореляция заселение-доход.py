import pandas
from numpy.linalg import qr, inv
from sklearn.linear_model import LinearRegression
import numpy
import matplotlib.pyplot as plt
from scipy.stats import t
from math import sqrt



df=pandas.read_excel('data.xlsx')
data=df.to_numpy()

#i = 2 111 .. 3 040
x=[]
y=[]
for i in range(2151, 3040):
    x.append(data[i][1])
    y.append(round(data[i][8]))


x1=numpy.vstack([x, numpy.ones(len(x))]).transpose()

Q, R = qr(x1)
b=inv(R) @ Q.transpose() @ y
k1=b[0]
b1=b[1]
print('QR разложение:\nk = ', k1, '\nb = ', b1)


X=pandas.DataFrame(x)
Y=pandas.DataFrame(y)



fit=LinearRegression().fit(X, Y)
k2=fit.coef_.flatten()
b2=fit.intercept_.flatten()
print('LinearRegression:\nk = ', k2, '\nb = ', b2)



xy=[]
for i in range(len(x)):
    xy.append([x[i], y[i]])
XY=pandas.DataFrame(xy)

r=XY.corr(method='pearson')
print('коэффициент корреляции: \n',r)

n=len(x)
lower=t(n-1).ppf(0.025)
upper=t(n-1).ppf(0.975)
r1=r[0][1]
test=r1/sqrt((1-r1**2)/(n-2))
if ((test<lower) or (test>upper)):
    print('Корреляция обоснована.')
else:
    print('Корреляция не обоснована.')
if test>0:
    p_value=1.0-t(n-1).cdf(test)
else:
    p_value=t(n-1).cdf(test)
p_value*=2
print('p-значение = ', p_value)

for i in (0.35, 0.5, 0.8, 0.95, 1.0):
    predicted_y=round(k1*i+b1)
    print('При х = ', i, '\tpredicted_y = ', predicted_y)

plt.scatter(X, Y)
plt.scatter(X, k1*X+b1)
plt.plot(X, k2*X+b2, color='brown')
plt.show()







