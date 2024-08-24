import time
import geopy
from geopy.geocoders import Nominatim
import overpy
import psycopg2
import random

conn = psycopg2.connect(
    host="localhost",
    database="garden_ring", # !!! переименовать в osm !!!
    user="postgres",
    password="postgres")
cursor = conn.cursor()

def add_city_to_db(city):
    cursor.execute('''SELECT city_id FROM city WHERE name = %s;''', (city,))
    city_record = cursor.fetchone()
    if city_record:
        city_id = city_record[0]
    else:
        cursor.execute('''INSERT INTO city (name) VALUES (%s) RETURNING city_id;''', (city,))
        city_id = cursor.fetchone()[0]
    conn.commit()
    return city_id

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
    cursor.execute('''INSERT INTO poi_coordinates (poi_id, latitude, longitude) VALUES (%s, %s, %s);''', (poi_id, latitude, longitude))
    conn.commit()

def add_poi_category_to_db(poi_id, category_name):
    cursor.execute('''INSERT INTO poi_category (poi_id, category) VALUES (%s, %s);''', (poi_id, category_name))
    conn.commit()

def add_poi_type_to_db(poi_id, poi_type):
    cursor.execute('''INSERT INTO poi_type (poi_id, type) VALUES (%s, %s);''', (poi_id, poi_type))
    conn.commit()

def get_district(latitude, longitude):
    geolocator = Nominatim(user_agent="my_unique_user_agent")
    pause = random.uniform(1,3)
    time.sleep(pause)
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    district = address.get('suburb', '') or address.get('district', '')
    return district

key = {'historic', 'building', 'tourism'}

def get_monuments_coordinates(city, category):
    OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

    overpass = f"""
        area[name="{city}"];
        (
        node["{category}"](area);
        way["{category}"](area);
        rel["{category}"](area);
        );
        out center;"""
    
    pause = random.uniform(1,3)
    time.sleep(pause)
    api = overpy.Overpass(url=OVERPASS_API_URL)
    
    response = api.query(overpass)
    if response.nodes or response.ways or response.relations:
        elements = response.nodes + response.ways + response.relations
        poi_data = [(elem.tags.get('name', 'Unknown'), elem.lat, elem.lon, *elem.tags.items()) 
                    for elem in elements 
                    if hasattr(elem, 'lat') and hasattr(elem, 'lon')]
        return poi_data
    else:
        return None

def get_available_categories():
    return ['historic', 'building', 'tourism']

def main():
    city = input("Введите название города: ")

    # print("Доступные категории мест к посещению:")
    available_categories = get_available_categories()
    # for index, category in enumerate(available_categories, start=1):
    #     print(f"{index}. {category}")

    while True:
        category_index = input("Введите номер категории: ")
        if category_index.isdigit():
            category_index = int(category_index)
            if 1 <= category_index <= len(available_categories):
                selected_category = available_categories[category_index - 1]
                break
            else:
                print("Некорректный ввод. Пожалуйста, повторите еще раз.")
        else:
            print("Некорректный ввод. Пожалуйста, повторите еще раз.")


    city_id = add_city_to_db(city)

    for data in get_monuments_coordinates(city, selected_category):
        name, latitude, longitude, *poi_types = data
        
        try:
            district = get_district(latitude, longitude)
        except geopy.exc.GeocoderUnavailable as e:
            # print(f"Произошла ошибка при получении района для координат ({latitude}, {longitude}): {e}")
            continue
        
        selected_tags = [(tag[0], tag[1]) for tag in poi_types if tag[0] in key]

        try:
            if district:
                district_id = add_district_to_db(city_id, district)
                poi_id = add_poi_to_db(district_id, name)
                add_coordinates_to_db(poi_id, latitude, longitude)

                for category, poi_type in selected_tags:
                    add_poi_category_to_db(poi_id, category)
                    add_poi_type_to_db(poi_id, poi_type)

                # print(f"Данные '{name}' получены")
            else:
                print(f"'{name}' за пределами '{city}'")
       
        except Exception as error:
            print(error)
            time.sleep(60)
            continue

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
