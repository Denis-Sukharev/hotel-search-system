#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import csv
import pandas as pd
import plotly.express as px


# In[3]:


import psycopg2
import csv

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host="217.71.129.139",
            database="postgres",
            port = "4580",
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

def get_poi_types(conn, district_names=None):
    cursor = conn.cursor()

    query = """
        SELECT poi_type.type, COUNT(*)
        FROM poi_type
        JOIN poi ON poi_type.poi_id = poi.poi_id
        JOIN district ON poi.district_id = district.district_id
    """
    
    if district_names:
        query += " WHERE district.name IN %s"

    query += """
        GROUP BY poi_type.type
        HAVING poi_type.type IN (
            'monument', 'church', 'manor', 'museum', 'machine', 'artwork', 'hotel', 'hostel', 'suburb',  'kiosk', 'cannon', 'ruins', 'archaeological_site', 'wayside_cross', 'zoo', 'vehicle', 'theme_park',  'gallery', 'milestone', 'tomb', 'viewpoint', 'memorial', 'chapel', 'castle', 'monastery', 'city_gate', 'attraction', 'neighbourhood'
        )
    """
    
    if district_names:
        cursor.execute(query, (tuple(district_names),))
    else:
        cursor.execute(query)

    poi_types_with_counts = cursor.fetchall()
    cursor.close()

    return poi_types_with_counts

def get_poi_categories(conn, district_names=None, poi_types=None):
    cursor = conn.cursor()

    query = """
        SELECT poi_category.category, COUNT(*)
        FROM poi_category
        JOIN poi ON poi_category.poi_id = poi.poi_id
        JOIN district ON poi.district_id = district.district_id
    """
    
    conditions = []
    params = []

    if district_names:
        conditions.append("district.name IN %s")
        params.append(tuple(district_names))
    if poi_types:
        conditions.append("poi.poi_id IN (SELECT poi_id FROM poi_type WHERE type IN %s)")
        params.append(tuple(poi_types))
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
        GROUP BY poi_category.category
        HAVING poi_category.category IN ('building', 'tourism', 'historic')
    """
    
    cursor.execute(query, params)

    poi_category_with_counts = cursor.fetchall()
    cursor.close()

    return poi_category_with_counts

def get_pois_by_criteria(conn, city_name, district_names=None, poi_types=None, poi_categories=None):
    cursor = conn.cursor()

    query = """
        SELECT poi.poi_id, poi.name, poi_coordinates.latitude, poi_coordinates.longitude, poi.district_id
        FROM poi 
        JOIN poi_coordinates ON poi.poi_id = poi_coordinates.poi_id
        JOIN district ON poi.district_id = district.district_id
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
    if poi_categories:
        query += " AND poi.poi_id IN (SELECT poi_id FROM poi_category WHERE category IN %s)"
        params.append(tuple(poi_categories))

    cursor.execute(query, params)
    data = cursor.fetchall()

    cursor.close()
    return data

def main():
    conn = connect_to_database()
    if not conn:
        return

    # print()
    # print("Доступные города:", ', '.join(get_cities(conn)))
    city_name = input()#"Введите название города: ")

    # print()
    # print("Доступные районы:")
    districts = get_districts(conn)
    # for i, district in enumerate(districts):
    #     print(f"{i}: {district}")
    district_input = input()#"Введите номера районов через запятую или оставьте пустым для выбора всех: ")
    district_indices = district_input.split(',') if district_input else None
    district_names = [districts[int(index)] for index in district_indices] if district_indices else None
    
    # print()
    # print("Доступные типы точек интереса:")
    poi_types = get_poi_types(conn, district_names)
    # for i, (poi_type, count) in enumerate(poi_types):
    #     print(f"{i}: {poi_type} ({count})")
    poi_input = input()#"Введите номера типов точек интереса через запятую или оставьте пустым для выбора всех: ")
    poi_indices = poi_input.split(',') if poi_input else None
    poi_types_selected = [poi_types[int(index)][0] for index in poi_indices] if poi_indices else None

    # print()
    # print("Доступные категории точек интереса:")
    poi_categories = get_poi_categories(conn, district_names, poi_types_selected)
    # for i, (poi_category , count) in enumerate(poi_categories):
    #     print(f"{i}: {poi_category} ({count})")
    poi_input = input()#"Введите номера категорий точек интереса через запятую или оставьте пустым для выбора всех: ")
    poi_indices = poi_input.split(',') if poi_input else None
    poi_categories_selected = [poi_categories[int(index)][0] for index in poi_indices] if poi_indices else None
    if not poi_categories_selected:
        poi_categories_selected = ['building', 'tourism', 'historic']

    data = get_pois_by_criteria(conn, city_name, district_names, poi_types_selected, poi_categories_selected)

    with open('/Users/kirillbogomolov/mestechko/finding_ways/poi/poi.csv', 'w', newline='', encoding='utf-8-sig') as file:
        record = csv.writer(file)
        record.writerow(['poi_id', 'name', 'latitude', 'longitude', 'district_id'])
        record.writerows(data)

    conn.close()

if __name__ == "__main__":
    main()



# In[4]:


# бесплатный ключ доступа можно найти здесь https://account.mapbox.com
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiY3NpY3NhY3NvIiwiYSI6ImNsaWFpM3B2bzAzcTUzbXFwZ2ZjdnVpajEifQ.UY-B4Tg9KH0NXNC423X7Jg"


# In[8]:


data_district_sum = pd.read_csv('/Users/kirillbogomolov/mestechko/finding_ways/poi/poi.csv')
district_sum = data_district_sum.groupby('district_id').size().reset_index(name='Плотность')
data_district_sum = pd.merge(data_district_sum, district_sum, on='district_id')


# In[9]:


fig = px.scatter_mapbox(
    data_district_sum,
    lat='latitude',
    lon='longitude',
    # color='Плотность', #size='Плотность',
    # width=1000, height=800, 
    hover_name='name',
    zoom = 9,
    # mapbox_style='open-street-map'
    mapbox_style='carto-positron'
)
fig.show()

