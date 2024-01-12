import overpy
import psycopg2

city="Новосибирск"

conn=psycopg2.connect(
    host="localhost",
    database="osm",
    user="postgres",
    password="postgres")

cursor=conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS memorial 
               (id SERIAL PRIMARY KEY,
               name VARCHAR(255),
               latitude DOUBLE PRECISION,
               longitude DOUBLE PRECISION);''')

delete_data='DELETE FROM memorial;'
cursor.execute(delete_data)


def get_monuments_coordinates(city):
    OVERPASS_API_URL ="https://overpass.openstreetmap.ru/cgi/interpreter"

    overpass =f"""
        area[name="{city}"];
        (
          node["historic"="memorial"](area);
          way["historic"="memorial"](area);
          rel["historic"="memorial"](area);
        );
        out center;"""

    api =overpy.Overpass(url=OVERPASS_API_URL)
    response =api.query(overpass)

    if response.nodes or response.ways or response.relations:
        elements=response.nodes + response.ways + response.relations
        monuments_data=[(elem.tags.get('name', 'Unknown'), elem.lat, elem.lon) 
                          for elem in elements 
                          if hasattr(elem, 'lat') and hasattr(elem, 'lon')]
        return monuments_data
    else:
        return None

monuments_data=get_monuments_coordinates(city)

if monuments_data:
    cursor.execute('SELECT MAX(id) FROM memorial;')
    max_id=cursor.fetchone()[0]
    max_id=max_id or 0

    for data in monuments_data:
        name, latitude, longitude =data
        max_id +=1
        cursor.execute('''INSERT INTO memorial (id, name, latitude, longitude) VALUES (%s, %s, %s, %s);''', 
            (max_id, name, latitude, longitude))
    print("данные внесены в таблицу")

conn.commit()
cursor.close()
conn.close()

