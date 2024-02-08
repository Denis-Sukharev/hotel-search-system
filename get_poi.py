import overpy
import psycopg2
import random
import time

city = "Москва"

conn = psycopg2.connect(
    host="localhost",
    database="osm",
    user="postgres",
    password="postgres")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS poi
               (poi_id SERIAL PRIMARY KEY,
               name VARCHAR(1000) NOT NULL);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS poi_coordinates
               (id SERIAL PRIMARY KEY,
               poi_id INTEGER NOT NULL,
               latitude DOUBLE PRECISION NOT NULL,
               longitude DOUBLE PRECISION NOT NULL,
               FOREIGN KEY (poi_id) REFERENCES poi(poi_id));''')
cursor.execute('''DELETE FROM poi_coordinates;''')
cursor.execute('''DELETE FROM poi;''')

def get_monuments_coordinates(city):
    OVERPASS_API_URL = "https://overpass.openstreetmap.ru/cgi/interpreter"

    overpass = f"""
        area[name="{city}"];
        (
          node["historic"="memorial"](area);
          way["historic"="memorial"](area);
          rel["historic"="memorial"](area);
        );
        out center;"""

    # delay = random.uniform(0.1, 0.5)
    # time.sleep(delay)

    api = overpy.Overpass(url=OVERPASS_API_URL)
    response = api.query(overpass)

    if response.nodes or response.ways or response.relations:
        elements = response.nodes + response.ways + response.relations
        monuments_data = [(elem.tags.get('name', 'Unknown'), elem.lat, elem.lon) 
                          for elem in elements 
                          if hasattr(elem, 'lat') and hasattr(elem, 'lon')]
        return monuments_data
    else:
        return None

if get_monuments_coordinates(city):
    for data in get_monuments_coordinates(city)[:10]:
        name, latitude, longitude = data

        cursor.execute('''INSERT INTO poi (name) VALUES (%s) RETURNING poi_id;''', (name,))
        poi_id = cursor.fetchone()[0]
        cursor.execute('''INSERT INTO poi_coordinates (poi_id, latitude, longitude) VALUES (%s, %s, %s);''', (poi_id, latitude, longitude))

conn.commit()
cursor.close()
conn.close()
