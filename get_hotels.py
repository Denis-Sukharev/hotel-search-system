import requests
from bs4 import BeautifulSoup
import re
import time
import random
import psycopg2

url = 'https://m.101hotels.com/main/cities/moskva/alphabetically'

html = requests.get(url)

s = BeautifulSoup(html.content, 'html.parser')
results = s.find(id='hotels-list')
hotel_links = results.find_all('a', class_='link__trigger')


def add_data_to_db(name, latitude, longitude):
    conn = psycopg2.connect(
        host="localhost",
        database="osm",
        user="postgres",
        password="postgres")
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO poi (name) VALUES (%s) RETURNING poi_id;''', (name,))
    poi_id = cursor.fetchone()[0]
    
    cursor.execute('''INSERT INTO poi_coordinates (poi_id, latitude, longitude) VALUES (%s, %s, %s);''', (poi_id, latitude, longitude))
    
    conn.commit()
    cursor.close()
    conn.close()


for link in hotel_links[:3]:
    href = link['href']
    new_url = f'https://m.101hotels.com{href}#map'
    
    pause = random.uniform(0.1, 0.5)
    time.sleep(pause)
    
    new_html = requests.get(new_url)
    
    hotel_name = link.find(class_='link__title').get_text(strip=True) 
    coord = re.search(r'center:\s\[(\d+\.\d+)\,(\d+\.\d+)\]', new_html.text)
    
    if coord:
        lat, lon = coord.groups()
        add_data_to_db(hotel_name, lat, lon)
