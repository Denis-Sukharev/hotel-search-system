CREATE TABLE city (
    city_id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL);

CREATE TABLE district (
    district_id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL,
    name VARCHAR(30) NOT NULL,
    FOREIGN KEY (city_id) REFERENCES city(city_id));

CREATE TABLE poi (
    poi_id SERIAL PRIMARY KEY,
    district_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (district_id) REFERENCES district(district_id));

CREATE TABLE poi_type (
    id SERIAL PRIMARY KEY,
    poi_id INTEGER NOT NULL,
    type VARCHAR(100) NOT NULL,
    FOREIGN KEY (poi_id) REFERENCES poi(poi_id));

CREATE TABLE poi_coordinates (
    id SERIAL PRIMARY KEY,
    poi_id INTEGER NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    FOREIGN KEY (poi_id) REFERENCES poi(poi_id));

CREATE TABLE poi_time (
    id SERIAL PRIMARY KEY,
    poi_id INTEGER NOT NULL,
    opening_time TIME,
    closing_time TIME,
    FOREIGN KEY (poi_id) REFERENCES poi(poi_id));

CREATE TABLE poi_duration (
    id SERIAL PRIMARY KEY,
    poi_id INTEGER NOT NULL,
    duration INTEGER,
    FOREIGN KEY (poi_id) REFERENCES poi(poi_id));

CREATE TABLE hotel_stars (
    id SERIAL PRIMARY KEY,
    poi_id INTEGER NOT NULL,
    stars DOUBLE PRECISION,
    FOREIGN KEY (poi_id) REFERENCES poi(poi_id));

CREATE TABLE hotel_rating (
    id SERIAL PRIMARY KEY,
    poi_id INTEGER NOT NULL,
    rating DOUBLE PRECISION,
    time TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (poi_id) REFERENCES poi(poi_id));

CREATE TABLE hotel_price (
    id SERIAL PRIMARY KEY,
    poi_id INTEGER NOT NULL,
    price INTEGER,
    FOREIGN KEY (poi_id) REFERENCES poi(poi_id));


ALTER TABLE district
ADD FOREIGN KEY (city_id) REFERENCES city(city_id);

ALTER TABLE poi
ADD FOREIGN KEY (district_id) REFERENCES district(district_id);

ALTER TABLE poi_type
ADD FOREIGN KEY (poi_id) REFERENCES poi(poi_id);

ALTER TABLE poi_coordinates
ADD FOREIGN KEY (poi_id) REFERENCES poi(poi_id);

ALTER TABLE poi_time
ADD FOREIGN KEY (poi_id) REFERENCES poi(poi_id);

ALTER TABLE poi_duration
ADD FOREIGN KEY (poi_id) REFERENCES poi(poi_id);

ALTER TABLE hotel_stars
ADD FOREIGN KEY (poi_id) REFERENCES poi(poi_id);

ALTER TABLE hotel_rating
ADD FOREIGN KEY (poi_id) REFERENCES poi(poi_id);

ALTER TABLE hotel_price
ADD FOREIGN KEY (poi_id) REFERENCES poi(poi_id);
