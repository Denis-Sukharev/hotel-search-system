from fastapi import APIRouter
import psycopg2
from pydantic import BaseModel

router = APIRouter()

conn = psycopg2.connect(
    host="217.71.129.139",
    database="postgres",
    port = "4580",
    user="postgres",
    password="postgres")



@router.get("/poi/all/{page}") # вывод 20 poi для страниц
async def select_poi(page:int):
    with conn:
        with conn.cursor() as cur:
            #cur.execute("SELECT * FROM poi OFFSET %s LIMIT 20;", (int(page) * 20,))
            cur.execute("SELECT * FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category <> 'Проживание' OFFSET %s LIMIT 20;", (int(page) * 20,))
            poi = cur.fetchall()
            return poi

@router.get("/poi/search_name/{name_fragment}")# поиск poi по названию
async def select_name_poi(name_fragment):
    with conn:
        with conn.cursor() as cur:
            #cur.execute("SELECT poi_id, name FROM poi  WHERE LOWER(name) ILIKE %s LIMIT 5;", ('%' + name_fragment.lower() + '%',))
            cur.execute("""
                        SELECT poi.poi_id, poi.name FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category <> 'Проживание' WHERE poi.name ILIKE %s LIMIT 5;
                        """, ('%' + name_fragment.lower() + '%',))
            poi = cur.fetchall()
            return poi
        
@router.get("/poi/search_id/{id_poi}")# поиск poi по id
async def select_id_poi(id_poi:int):
    with conn:
        with conn.cursor() as cur:
            #cur.execute("select * from poi where poi_id = %s;", (id_poi,))
            cur.execute("""
                        SELECT * FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category <> 'Проживание' WHERE poi.poi_id = %s;
                        """, (id_poi,))
            poi = cur.fetchall()
            return poi 
         
@router.get("/hotel/all/{page}")# вывод 20 hotel для страниц
async def select_hotel(page):
    with conn:
        with conn.cursor() as cur:
            #cur.execute("select * from poi_coordinates limit 5")
            cur.execute("select * from poi inner join poi_category on poi.poi_id = poi_category.poi_id and poi_category.category = 'Проживание' OFFSET %s LIMIT 20;", (int(page) * 20,))
            poi = cur.fetchall()
            return poi 

@router.get("/hotel/search_name/{name_fragment}")# поиск hotel по name
async def select_name_hotel(name_fragment):
    with conn:
        with conn.cursor() as cur:  
            #cur.execute("select * from poi_coordinates limit 5")
            cur.execute("select poi.poi_id, poi.name from poi inner join poi_category on poi.poi_id = poi_category.poi_id and poi_category.category = 'Проживание' WHERE poi.name ILIKE %s LIMIT 5;", ('%' + name_fragment.lower() + '%',))
            poi = cur.fetchall()
            return poi 

@router.get("/hotel/search_id/{id_hotel}")# поиск hotel по id
async def select_id_hotel(id_poi):
    with conn:
        with conn.cursor() as cur:  
            #cur.execute("select * from poi_coordinates limit 5")
            cur.execute("""
                        SELECT * FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category = 'Проживание' WHERE poi.poi_id = %s;
                        """, (id_poi,))            
            poi = cur.fetchall()
            return poi 


@router.get("/hotel/count")# кол-во hotel
async def select_id_hotel():
    with conn:
        with conn.cursor() as cur:  
            cur.execute("""
                        SELECT count(poi.poi_id) FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category = 'Проживание';
                        """)            
            poi = cur.fetchall()
            return poi

@router.get("/poi/count")# кол-во poi
async def select_id_hotel():
    with conn:
        with conn.cursor() as cur:  
            cur.execute("""
                        SELECT count(poi.poi_id) FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category <> 'Проживание';
                        """)            
            poi = cur.fetchall()
            return poi
'''
class Hotel(BaseModel):
    name: str
    address: str
    rating: int
    
@router.get("/hotels/{hotel_id}")
async def read_hotel(hotel_id: int):
    return {"name": "Hotel 1", "address": "Address 1", "rating": 5}

@router.post("/hotels/")
async def create_hotel(hotel: Hotel):
    return hotel

@router.put("/hotels/{hotel_id}")
async def update_hotel(hotel_id: int, hotel: Hotel):
    return hotel

@router.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int):
    return {"message": "Hotel deleted"}'''

