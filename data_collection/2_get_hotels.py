from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup
import re
import psycopg2
import time
import random

conn = psycopg2.connect(
    host="localhost",
    database="osm",
    user="postgres",
    password="postgres")
cursor = conn.cursor()


def add_city_to_db(city):
    cursor.execute('''SELECT city_id FROM city WHERE name = %s;''', (city,))
    city_id = cursor.fetchone()
    
    if not city_id:
        cursor.execute('''INSERT INTO city (name) VALUES (%s) RETURNING city_id;''', (city,))
        city_id = cursor.fetchone()
        conn.commit()
    
    return city_id[0] if city_id else None

def add_district_to_db(city_id, district_name):    
    cursor.execute('''SELECT district_id FROM district WHERE city_id = %s AND name = %s;''', (city_id, district_name))
    district_record = cursor.fetchone()
    
    if district_record:
        district_id = district_record[0]
    
    else:
        cursor.execute('''INSERT INTO district (city_id, name) VALUES (%s, %s) RETURNING district_id;''', (city_id, district_name))
        district_id = cursor.fetchone()[0]
    
    conn.commit() 
    return district_id

def add_poi_to_db(district_id, name):
    cursor.execute('''INSERT INTO poi (district_id, name) VALUES (%s, %s) RETURNING poi_id;''', (district_id, name))
    poi_id = cursor.fetchone()[0]
    
    conn.commit()
    return poi_id

def add_coordinates_to_db(poi_id, latitude, longitude):
    conn.commit()
    cursor.execute('''INSERT INTO poi_coordinates (poi_id, latitude, longitude) VALUES (%s, %s, %s);''', (poi_id, latitude, longitude))

def add_poi_category_to_db(poi_id, category_name):
    cursor.execute('''INSERT INTO poi_category (poi_id, category) VALUES (%s, %s);''', (poi_id, category_name))
    conn.commit()

def add_poi_type_to_db(poi_id, poi_type):
    cursor.execute('''INSERT INTO poi_type (poi_id, type) VALUES (%s, %s);''', (poi_id, poi_type))
    conn.commit()

def add_hotel_rating_to_db(poi_id, rating):
    cursor.execute('''INSERT INTO hotel_rating (poi_id, rating) VALUES (%s, %s);''', (poi_id, rating))
    conn.commit()

def add_hotel_stars_to_db(poi_id, stars):
    cursor.execute('''INSERT INTO hotel_stars (poi_id, stars) VALUES (%s, %s);''', (poi_id, stars))
    conn.commit()  

def get_district(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")

    pause = random.uniform(1,2)
    time.sleep(pause)

    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    district = address.get('suburb', '')
    
    if not district:
        district = address.get('district', '')
    return district


city = 'Москва'
city_id = add_city_to_db(city)

url = 'https://m.101hotels.com/main/cities/moskva/alphabetically'

html = requests.get(url)

s = BeautifulSoup(html.content, 'html.parser')
results = s.find(id='hotels-list')
hotel_links = results.find_all('a', class_='link__trigger')

for link in hotel_links[:3]:
    href = link['href']
    new_url = f'https://m.101hotels.com{href}#map'

    pause = random.uniform(1,2)
    time.sleep(pause)
    
    new_html = requests.get(new_url)
    hotel_name = link.find(class_='link__title').get_text(strip=True)
    poi_type = link.find(class_='link__description').get_text(strip=True)
        
    rating_match = re.search(r'<span class="hotel-rating-item__rating-number">(\d+\.\d+)</span>', new_html.text)
    rating = rating_match.group(1)

    stars_match = re.search(r'<div class="hotel__stars">(.+)</div>', new_html.text)
    stars_string = stars_match.group(1) if stars_match else ''
    stars_count = stars_string.count('icon icon_star colored')
    
    coord = re.search(r'center:\s\[(\d+\.\d+)\,(\d+\.\d+)\]', new_html.text)
    if coord:
        lat, lon = coord.groups()
        district = get_district(lat, lon)
        
        if district:
            district_id = add_district_to_db(city_id, district)
            poi_id = add_poi_to_db(district_id, hotel_name)
            add_coordinates_to_db(poi_id, lat, lon)
            add_poi_category_to_db(poi_id, 'residence')
            add_poi_type_to_db(poi_id, poi_type)
            add_hotel_rating_to_db(poi_id, rating)
            
            if stars_count > 0:
                add_hotel_stars_to_db(poi_id, stars_count)

            print(f"УСПЕШНО: {hotel_name}")
       
        else:
            print(f"'{hotel_name}' ЗА ПРЕДЕЛАМИ '{city}'")

cursor.close()
conn.close()
