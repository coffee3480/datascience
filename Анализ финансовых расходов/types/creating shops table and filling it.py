from pathlib import Path
import os
import psycopg2

conn=psycopg2.connect(host='localhost', database='purchs', user='postgres', password='nullcore')
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS shops (shop VARCHAR PRIMARY KEY, type VARCHAR DEFAULT 'Неизвестно');")
cur.execute('TRUNCATE TABLE shops;')
conn.commit()

for file in os.scandir():
    if Path(file).suffix=='.txt':
        stem=Path(file).stem
        #print(stem)
        with open(file, 'r', encoding='utf-8') as f:
              content=f.read()
              lines=content.split('\n')
              for line in lines:
                  #print(line)
                  cur.execute('INSERT INTO shops (shop, type) VALUES (%s, %s);', (line, stem))
conn.commit()



cur.execute('SELECT * FROM shops;')
print(cur.fetchall())
cur.close()
conn.close()

