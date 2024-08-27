import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="garden_ring", # !!! переименовать в osm !!!
    user="postgres",
    password="postgres")

cursor = conn.cursor()

# cursor.execute('''
#                DROP TABLE hotel_rating;
#                DROP TABLE hotel_stars;
#                DROP TABLE poi_type;
#                DROP TABLE poi_category;
#                DROP TABLE poi_coordinates;
#                DROP TABLE  poi;
#                DROP TABLE  district;
#                DROP TABLE  city;''')

cursor.execute('''CREATE TABLE city (
               city_id SERIAL PRIMARY KEY,
               name VARCHAR(500) NOT NULL);''')
cursor.execute('''CREATE TABLE district (
               district_id SERIAL PRIMARY KEY,
               city_id INTEGER NOT NULL,
               name VARCHAR(500) NOT NULL,
               FOREIGN KEY (city_id) REFERENCES city(city_id));''')
cursor.execute('''CREATE TABLE poi (
               poi_id SERIAL PRIMARY KEY,
               district_id INTEGER NOT NULL,
               name VARCHAR(500) NOT NULL,
               FOREIGN KEY (district_id) REFERENCES district(district_id));''')
cursor.execute('''CREATE TABLE poi_coordinates (
               id SERIAL PRIMARY KEY,
               poi_id INTEGER NOT NULL,
               latitude DOUBLE PRECISION NOT NULL,
               longitude DOUBLE PRECISION NOT NULL,
               FOREIGN KEY (poi_id) REFERENCES poi(poi_id));''')
cursor.execute('''CREATE TABLE poi_type (
               id SERIAL PRIMARY KEY,
               poi_id INTEGER NOT NULL,
               type VARCHAR(300) NOT NULL,
               FOREIGN KEY (poi_id) REFERENCES poi(poi_id));''')
cursor.execute('''CREATE TABLE poi_category (
               id SERIAL PRIMARY KEY,
               poi_id INTEGER NOT NULL,
               category VARCHAR(100) NOT NULL,
               FOREIGN KEY (poi_id) REFERENCES poi(poi_id));''')
cursor.execute('''CREATE TABLE hotel_stars (
               id SERIAL PRIMARY KEY,
               poi_id INTEGER NOT NULL,
               stars DOUBLE PRECISION,
               FOREIGN KEY (poi_id) REFERENCES poi(poi_id));''')
cursor.execute('''CREATE TABLE hotel_rating (
               id SERIAL PRIMARY KEY,
               poi_id INTEGER NOT NULL,
               rating DOUBLE PRECISION,
               time TIMESTAMP DEFAULT NOW(),
               FOREIGN KEY (poi_id) REFERENCES poi(poi_id));''')

conn.commit()
cursor.close()
conn.close()

# МОЖНО ДОБАВИТЬ:
# '''CREATE TABLE poi_time (
#     id SERIAL PRIMARY KEY,
#     poi_id INTEGER NOT NULL,
#     opening_time TIME,
#     closing_time TIME,
#     FOREIGN KEY (poi_id) REFERENCES poi(poi_id));

# CREATE TABLE poi_duration (
#     id SERIAL PRIMARY KEY,
#     poi_id INTEGER NOT NULL,
#     duration INTEGER,
#     FOREIGN KEY (poi_id) REFERENCES poi(poi_id));

# CREATE TABLE hotel_price (
#     id SERIAL PRIMARY KEY,
#     poi_id INTEGER NOT NULL,
#     price INTEGER,
#     FOREIGN KEY (poi_id) REFERENCES poi(poi_id));'''