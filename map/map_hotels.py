#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import csv
import pandas as pd
import plotly.express as px


# In[ ]:


def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="osm",
            user="postgres",
            password="postgres"
        )
        return conn
    except psycopg2.Error as e:
        print("Ошибка при подключении к базе данных:", e)
        return None

def get_cities(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM city")
    cities = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return cities

def get_districts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM district")
    districts = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return districts

def get_poi_types(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, COUNT(*) 
        FROM poi_type 
        GROUP BY type 
        HAVING type IN (
            'Загородный отель', 'Апарт-отель', 'Арт-отель', 'Бизнес-отель', 
            'Семейный отель', 'Мини-гостиница', 'Санаторий', 'Гостевые комнаты',
            'Капсульный хостел', 'Загородный дом', 'Комплекс апартаментов', 'Комплекс',
            'Загородный клуб', 'Капсульный отель', 'Бутик-Отель', 'Отель', 
            'Общежитие гостиничного типа', 'Эконом-отель', 'Дом отдыха', 'Гостевой дом',
            'Гостиничный комплекс', 'Квартира', 'Мини-отель', 'Отель & Хостел',
            'Дизайн-Отель', 'Гостиница', 'Спа-отель', 'Отель и апартаменты',
            'Хостелы', 'Парк-Отель', 'Исторический отель', 'Арт Отель & Хостел',
            'Хостел'
        )
    """)
    poi_types_with_counts = cursor.fetchall()
    cursor.close()

    return poi_types_with_counts


def get_star_counts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT stars FROM hotel_stars")
    stars = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    star_ranges = ['1', '2', '3', '4', '5']
    star_counts = []
    
    for star_range in star_ranges:
        hotels_in_range = sum(1 for star in stars if star == star_range)
        star_counts.append((star_range, hotels_in_range))
    
    return star_counts

def get_rating_ranges(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT rating FROM hotel_rating")
    ratings = [row[0] for row in cursor.fetchall()]
    cursor.close()
    ranges = ['0-2', '2-4', '4-6', '6-8', '8-10']
    rating_ranges = []
    for r in ranges:
        min_rating, max_rating = map(int, r.split('-'))
        hotels_in_range = sum(1 for rating in ratings if min_rating <= rating <= max_rating)
        rating_ranges.append((r, hotels_in_range))
    return rating_ranges

def get_pois_by_criteria(conn, city_name, district_names=None, poi_types=None, star_counts=None, rating_ranges=None):
    cursor = conn.cursor()

    query = """
        SELECT poi.poi_id, poi.name, poi_coordinates.latitude, poi_coordinates.longitude, poi.district_id
        FROM poi 
        JOIN poi_coordinates ON poi.poi_id=poi_coordinates.poi_id
        JOIN district ON poi.district_id = district.district_id
        JOIN hotel_rating ON poi.poi_id = hotel_rating.poi_id
        WHERE district.city_id = (
            SELECT city_id FROM city WHERE name = %s
        )
    """
    params = [city_name]

    if district_names:
        query += " AND district.name IN %s"
        params.append(tuple(district_names))
    if poi_types:
        query += " AND poi.poi_id IN (SELECT poi_id FROM poi_type WHERE type IN %s)"
        params.append(tuple(poi_types))
    if star_counts:
        query += " AND stars IN %s"
        params.append(tuple(star_counts))
    if rating_ranges:
        range_conditions = []
        for rating_range in rating_ranges:
            min_rating, max_rating = map(int, rating_range.split('-'))
            range_conditions.append("rating BETWEEN %s AND %s")
            params.extend([min_rating, max_rating])
        query += " AND (" + " OR ".join(range_conditions) + ")"

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()
    return data

def main():
    conn = connect_to_database()
    if not conn:
        return

    print()
    print("Доступные города:", ', '.join(get_cities(conn)))
    city_name = input("Введите название города: ")

    print()
    print("Доступные районы:")
    districts = get_districts(conn)
    for i, district in enumerate(districts):
        print(f"{i}: {district}")
    district_input = input("Введите номера районов через запятую или оставьте пустым для выбора всех: ")
    district_indices = district_input.split(',') if district_input else None
    district_names = [districts[int(index)] for index in district_indices] if district_indices else None

    print()
    print("Доступные типы точек интереса:")
    poi_types = get_poi_types(conn)
    for i, (poi_type, count) in enumerate(poi_types):
        print(f"{i}: {poi_type} ({count})")
    poi_input = input("Введите номера типов мест проживания через запятую или оставьте пустым для выбора всех: ")
    poi_indices = poi_input.split(',') if poi_input else None
    poi_types_selected = [poi_types[int(index)][0] for index in poi_indices] if poi_indices else None

    print()
    star_counts = get_star_counts(conn)
    print("Доступные значения звезд:")
    for i, (star_range, count) in enumerate(star_counts):
        print(f"{i}: {star_range} ({count} мест проживания)")
    star_input = input("Введите количество звезд отеля через запятую или оставьте пустым для выбора всех: ").strip()
    star_indices = star_input.split(',') if star_input else None  
    star_indices_selected = []
    if star_indices:
        star_indices_selected = [rating_ranges[int(index)][0] for index in star_indices]

    print()
    print("Доступные диапазоны рейтинга:")
    rating_ranges = get_rating_ranges(conn)
    for i, (range_name, count) in enumerate(rating_ranges):
        print(f"{i}: {range_name} ({count} мест проживания)")
    rating_range_input = input("Введите номера диапазонов рейтинга через запятую или оставьте пустым для выбора всех: ").strip()
    rating_range_indices = rating_range_input.split(',') if rating_range_input else None
    rating_ranges_selected = []
    if rating_range_indices:
        rating_ranges_selected = [rating_ranges[int(index)][0] for index in rating_range_indices]

    data = get_pois_by_criteria(conn, city_name, district_names, poi_types_selected, star_indices_selected, rating_ranges_selected)

    with open('D:\\vkrb\\csv\\hotels.csv', 'w', newline='', encoding='utf-8-sig') as file:
        record = csv.writer(file)
        record.writerow(['poi_id', 'name', 'latitude', 'longitude', 'district_id'])
        record.writerows(data)

    conn.close()

if __name__ == "__main__":
    main()


# In[2]:


# бесплатный ключ доступа можно найти здесь https://account.mapbox.com
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiY3NpY3NhY3NvIiwiYSI6ImNsaWFpM3B2bzAzcTUzbXFwZ2ZjdnVpajEifQ.UY-B4Tg9KH0NXNC423X7Jg"


# In[3]:


data_district_sum = pd.read_csv('D:\\vkrb\\csv\\hotels.csv')
district_sum = data_district_sum.groupby('district_id').size().reset_index(name='Плотность')
data_district_sum = pd.merge(data_district_sum, district_sum, on='district_id')


# In[10]:


fig = px.scatter_mapbox(data_district_sum, lat='latitude', lon='longitude',
                        # color='Плотность', #size='Плотность',
                        # width=1000, height=800, 
                        hover_name='name',
                        zoom = 9,
                        # mapbox_style='open-street-map'
                        mapbox_style='carto-positron',
                        color_discrete_sequence=['red']
                        )
fig.show()

