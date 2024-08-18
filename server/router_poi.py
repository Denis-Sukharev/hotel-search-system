from typing import Union
from fastapi import APIRouter, Body
from server.database import conn


router = APIRouter(
    tags=['''POI''']
)




@router.get("/poi/all/{page}") # вывод 20 poi для страниц
async def select_poi(page):
    with conn:
        with conn.cursor() as cur:          
            cur.execute("SELECT * FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category <> 'Проживание' OFFSET %s LIMIT 20;", (int(page) * 20,))
            poi = cur.fetchall()
            return poi

@router.get("/poi/search_name/{name_fragment}")# поиск poi по названию
async def select_name_poi(name_fragment):
    with conn:
        with conn.cursor() as cur:
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
         


@router.get("/poi/count")# кол-во poi
async def select_count_poi():
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

