import random
import datetime
import pandas
import string


def generate_random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates + 1)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

dirpath=r'C:\Users\user\Desktop\Python programs\databases\postgres\hotels_web'

guests=pandas.DataFrame(columns=['surname', 'name', 'phone', 'email', 'comment', 'blacklisted', 'guest_id'])
people=pandas.read_csv(dirpath+r'\вспомогательные таблицы\people.csv')
names=list(people['First Name'])
surnames=list(people['Last Name'])
phone='+70000000000'
email=''
comment=''
blacklisted=False
for i in range(100):
    rand_name=random.randrange(1000)
    rand_surname=random.randrange(1000)
    new_row=pandas.Series({'surname':surnames[rand_surname], 'name':names[rand_name],
                           'phone':phone, 'email': email, 'comment': comment,
                           'blacklisted':blacklisted, 'guest_id':i+1})
    guests=guests._append(new_row, ignore_index=True)
guests.to_csv(dirpath+'\\guests.csv', index=False)    
    

passports=pandas.DataFrame(columns=['passp_series', 'passp_number', 'date_of_issue', 'date_of_birth',
                           'place_of_birth', 'nationality', 'name', 'surname', 'fathers_name',
                                    'passport_id'])

cities=pandas.read_excel(dirpath+r'\вспомогательные таблицы\cities.xlsx')
passp_series=''
fathers_name=''
nationality='US'
cities=list(cities['cities'])
for i in range(100):
    rand_passp_numb=random.randrange(999999)
    rand_name=names[random.randrange(1000)]
    rand_surname=surnames[random.randrange(1000)]
    rand_date_of_issue=generate_random_date(datetime.date(1980,1,1), datetime.date(2025,1,1))
    random_number_of_days = random.randrange(365, 365*20)
    rand_date_of_birth=rand_date_of_issue - datetime.timedelta(days=random_number_of_days)
    rand_place_of_birth=cities[random.randrange(len(cities))]
    new_row=pandas.Series({'passp_series':passp_series, 'passp_number':rand_passp_numb,
                           'date_of_issue':rand_date_of_issue, 'date_of_birth':rand_date_of_birth,
                           'place_of_birth':rand_place_of_birth, 'nationality':nationality,
                           'name':rand_name, 'surname':rand_surname, 'fathers_name':fathers_name,
                           'passport_id':i+1})
    passports=passports._append(new_row, ignore_index=True)
passports.to_csv(dirpath+'\\passports.csv', index=False)


bookings=pandas.DataFrame(columns=['booking_date', 'checkin', 'checkout', 'status', 'breakfast', 'price', 'comment',
                                   'guest_id', 'booking_number'])
comment=''
status_list=('checked-out', 'cancelled')
for i in range(40):
    s=''
    for i in range(6):
        if (random.randint(0,1)==0):
            s+=random.choice(string.ascii_uppercase)
        else:
            s+=str(random.randint(0,9))
    s+='_'
    rand_booking_date=generate_random_date(datetime.date(2020,1,1), datetime.date(2025,8,1))
    s+=str(rand_booking_date)[2:].replace('-','')
    rand_booking_numb=s
    random_number_of_days = random.randrange(365)
    rand_checkin=rand_booking_date + datetime.timedelta(days=random_number_of_days)
    random_number_of_days = random.randint(1,14)
    rand_checkout=rand_checkin + datetime.timedelta(days=random_number_of_days)
    rand_guest_id=random.randint(1,100)
    rand_status=random.choice(status_list)
    rand_price=random.randint(1000, 20000) if random.randint(1,10)<=8 else random.randint(20000,200000)
    breakfast=random.choice([True, False])
    new_row=pandas.Series({'booking_date':rand_booking_date, 'checkin':rand_checkin, 'checkout':rand_checkout,
                           'status':rand_status, 'breakfast':breakfast, 'price':rand_price, 'comment':comment, 
                           'guest_id':rand_guest_id, 'booking_number':rand_booking_numb})
    bookings=bookings._append(new_row, ignore_index=True)
bookings.to_csv(dirpath+'\\bookings.csv', index=False)


booking_passports=pandas.DataFrame(columns=['booking_numb', 'passp_id'])
booking_numbs=pandas.read_csv(dirpath+r'\bookings.csv')['booking_number']
for i in range(40):
    new_row=pandas.Series({'booking_numb':booking_numbs[i], 'passp_id':random.randint(1,100)})
    booking_passports=booking_passports._append(new_row, ignore_index=True)
booking_passports.to_csv(dirpath+r'\booking_passports.csv', index=False)


booking_rooms=pandas.DataFrame(columns=['booking_numb', 'room_id', 'row_id'])
for i in range(40):
    new_row=pandas.Series({'booking_numb':booking_numbs[i], 'room_id':random.randint(1,15),
                           'row_id':i+1})
    booking_rooms=booking_rooms._append(new_row, ignore_index=True)
booking_rooms.to_csv(dirpath+r'\booking_rooms.csv', index=False)








