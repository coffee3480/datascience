from pathlib import Path
import re
import pandas
import datetime
import psycopg2

input_path=Path('sms.html')
content_path=r'content.txt'
output_path=Path('output.xlsx')

conn=psycopg2.connect(host='localhost', database='purchs', user='postgres', password='nullcore')
cur=conn.cursor()

with open(input_path, 'r', encoding='utf-8') as file:
    content=file.read()

pattern1=r"<tr><td>Получено</td><td>\d* \S+ \d{4} г. \d{2}:\d{2}:\d{2}</td><td>[9][0][0]</td><td class='dont-break-out'>\S{4}\d{4} \d{2}:\d{2} Покупка \d+\.?\d*р .*?Баланс"
pattern2=r"<tr><td>Получено</td><td>\d* \S+ \d{4} г. \d{2}:\d{2}:\d{2}</td><td>[9][0][0]</td><td class='dont-break-out'>Счёт карты \S{4}\d{4} \d{2}:\d{2} Покупка \d+\.?\d*р .*?Баланс"
result_before_change=re.findall(pattern1, content, re.DOTALL)
result_after_change=re.findall(pattern2, content, re.DOTALL)
result=result_before_change+result_after_change
with open(content_path, 'w', encoding='utf-8') as file2:
    file2.write(content)

purch=pandas.DataFrame(columns=['Дата', 'Сумма', 'Магазин', 'Тип расходов'])
purch2=list()
for i in result:
    try:
        cont=re.search(r'Покупка \d+\.?\d*р.*?Баланс', i).group()
        summ=re.search(r'\d+\.?\d*' ,cont).group()
        summ=float(summ)
        shop=re.search(r'р .*? Баланс',cont).group()
        shop=shop.replace('р ', '')
        shop=shop.replace(' Баланс', '')
    except AttributeError:
        continue
    date=(re.search(r'\d* \S+ \d{4} г', i)).group()
    date=date.replace(' г', '')
    date=date.replace('.', '')
    date=date.split(' ')
    if len(date[0])==1:
        date[0]='0'+date[0]
    if date[1]=='янв':
        date[1]='01'
    elif date[1]=='февр':
        date[1]='02'
    elif date[1]=='мар':
        date[1]='03'
    elif date[1]=='апр':
        date[1]='04'
    elif date[1]=='мая':
        date[1]='05'
    elif date[1]=='июн':
        date[1]='06'
    elif date[1]=='июл':
        date[1]='07'
    elif date[1]=='авг':
        date[1]='08'
    elif date[1]=='сент':
        date[1]='09'
    elif date[1]=='окт':
        date[1]='10'
    elif date[1]=='нояб':
        date[1]='11'
    elif date[1]=='дек':
        date[1]='12'

    date=datetime.date(int(date[2]), int(date[1]), int(date[0]))
    cur.execute('SELECT EXISTS(SELECT type FROM shops WHERE shop=%s);', (shop,))
    flag=cur.fetchall()[0][0]
    if flag==True:
        cur.execute('SELECT type FROM shops WHERE shop=%s;', (shop,))
        purch_type=cur.fetchall()[0][0]
    else:
        cur.execute('INSERT INTO shops VALUES (%s);', (shop,))
        cur.execute('SELECT type FROM shops WHERE shop=%s;', (shop,))
        purch_type=cur.fetchall()[0][0]
    purch.loc[len(purch)]=[date, summ, shop, purch_type]
    purch2.append((date, summ, shop, purch_type))

purch.to_excel(output_path, index=False)


cur.execute('CREATE TABLE IF NOT EXISTS payments (id SERIAL PRIMARY KEY, date DATE, amount FLOAT, shop VARCHAR, purchase_type VARCHAR);')
cur.execute('TRUNCATE TABLE payments CASCADE;')
conn.commit()

query='INSERT INTO payments (date, amount, shop, purchase_type) VALUES (%s, %s, %s, %s);'
for i in purch2:
    cur.execute(query, (i[0], i[1], i[2], i[3]))

conn.commit()

def print_period_report(start_date, end_date, purchase_type):
    query="SELECT SUM(amount) FROM payments WHERE date >= DATE '" + start_date + "' AND date < DATE '" + end_date + "' AND purchase_type = '" + purchase_type + "';"
    cur.execute(query)
    try:
        print(purchase_type + ': ', round(cur.fetchall()[0][0],2))
    except TypeError:
        print(purchase_type + ': ', 0)

def print_monthly_report(month, year):
    
    if month in (1, '1', '01', 'Jan', 'January', 'jan', 'january', 'Янв', 'янв', 'Январь', 'январь', 'Янв.', 'янв.'):
        month=1
    elif month in (2, '2', '02', 'Feb', 'February', 'feb', 'february', 'Фев', 'фев', 'Февраль', 'февраль', 'Февр.', 'февр.'):
        month=2
    elif month in (3, '3', '03', 'Mar', 'March', 'mar', 'march', 'Мар', 'мар', 'Март', 'март'):
        month=3
    elif month in (4, '4', '04', 'Apr', 'April', 'apr', 'april', 'Апр', 'апр', 'Апрель', 'апрель', 'Апр.', 'апр.'):
        month=4
    elif month in (5, '5', '05', 'May', 'may', 'Май', 'май'):
        month=5
    elif month in (6, '6', '06', 'Jun', 'June', 'jun', 'june', 'Июн', 'июн', 'Июнь', 'июнь', 'Июн.', 'июн.'):
        month=6
    elif month in (7, '7', '07', 'Jul', 'July', 'jul', 'july', 'Июл', 'июл', 'Июль', 'июль', 'Июл.', 'июл.'):
        month=7
    elif month in (8, '8', '08', 'Aug', 'August', 'aug', 'august', 'Август', 'Авг', 'август', 'авг', 'Авг.', 'авг.'):
        month=8
    elif month in (9, '9', '09', 'Sep', 'September', 'sep', 'september', 'Сентябрь', 'Сент', 'сентябрь', 'сент', 'Сент.', 'сент.'):
        month=9
    elif month in (10, '10', 'Oct', 'October', 'oct', 'october', 'Октябрь', 'Окт', 'октябрь', 'окт', 'Окт.', 'окт.'):
        month=10
    elif month in (11, '11', 'Nov', 'November', 'nov', 'november', 'Ноябрь', 'Нояб', 'ноябрь', 'нояб', 'Нояб.', 'нояб.'):
        month=11
    elif month in (12, '12', 'Dec', 'December', 'dec', 'december', 'Декабрь', 'Дек', 'декабрь', 'дек', 'Дек.', 'дек.'):
        month=12
    year1=year
    year=str(year)
    if month>9:
        month1=str(month)
    else:
        month1='0'+str(month)
    
    start_date=year+'-'+month1+'-'+'01'
    
    month2=month+1
    if month2==13:
        month2=1
        year=str(int(year)+1)
    if month2>9:
        month2=str(month2)
    else:
        month2='0'+str(month2)
    
    end_date=year+'-'+month2+'-'+'01'

    print('Отчёт за ' + str(month) + '-ый месяц ' + str(year1) + ' года:')
    query="SELECT (purchase_type, SUM(amount)) FROM payments WHERE date >= DATE '" + start_date + "' AND date < DATE '" + end_date + "' GROUP BY purchase_type ORDER BY SUM(amount) DESC;"
    cur.execute(query)
    try:
        output=cur.fetchall()
        for i in output:
            for j in i:
                j=j.replace('(','')
                j=j.replace(')','')
                j=j.replace('"','')
                j=j.replace(',',':  ')
                print(j)
    except TypeError:
        pass
        
    cur.execute("SELECT SUM(amount) FROM payments WHERE date >= DATE '" + start_date + "' AND date < DATE '" + end_date + "';")
    try:
        print('\nИтого: ', round(cur.fetchall()[0][0], 2), '\n')
    except TypeError:
        print('Итого: 0')

print_monthly_report(12, 2025)
print_monthly_report(1, 2026)
print_monthly_report(2, 2026)



cur.close()
conn.close()

