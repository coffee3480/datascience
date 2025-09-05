import psycopg2
import pandas

try:
    conn=psycopg2.connect(host='localhost', database='hotels_web', user='postgres', password='rex')
    cursor=conn.cursor()
    cursor.execute('select * from bookings_general_info;')
    df=pandas.DataFrame(cursor)
    print(df)
except psycopg2.Error as e:
    print(e)
finally:
    cursor.close()
    conn.close()
