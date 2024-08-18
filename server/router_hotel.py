# import sys
# sys.path.append('../finding_ways/')
from finding_ways.start import optimal_hotel

from typing import Union
from fastapi import APIRouter
from server.database import conn
from server.schemas import HotelOptimal, Hotels
router = APIRouter(
    tags=['''HOTEL''']
)
   
@router.get("/hotel/all/{page}")# вывод 20 hotel для страниц
async def select_hotel(page:int):
    with conn:
        with conn.cursor() as cur:
            cur.execute("select * from poi inner join poi_category on poi.poi_id = poi_category.poi_id and poi_category.category = 'Проживание' OFFSET %s LIMIT 20;", (int(page) * 20,))
            hotel = cur.fetchall()
            return hotel

@router.get("/hotel/search_name/{name_fragment}")# поиск hotel по name
async def select_name_hotel(name_fragment):
    with conn:
        with conn.cursor() as cur:  
            cur.execute("select poi.poi_id, poi.name from poi inner join poi_category on poi.poi_id = poi_category.poi_id and poi_category.category = 'Проживание' WHERE poi.name ILIKE %s LIMIT 5;", ('%' + name_fragment.lower() + '%',))
            hotel = cur.fetchall()
            return hotel 

@router.get("/hotel/search_id/{id_hotel}")# поиск hotel по id
async def select_id_hotel(id_poi:int):
    with conn:
        with conn.cursor() as cur:  
            cur.execute("""
                        SELECT * FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category = 'Проживание' WHERE poi.poi_id = %s;
                        """, (id_poi,))            
            hotel = cur.fetchall()
            return hotel 


@router.get("/hotel/count")# кол-во hotel
async def select_count_hotel():
    with conn:
        with conn.cursor() as cur:  
            cur.execute("""
                        SELECT count(poi.poi_id) FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category = 'Проживание';
                        """)            
            hotel = cur.fetchall()
            return hotel
        

@router.post("/hotel/optimal", description="Требуется: лимит времени в часах, кол-во дней, poi_id. Ответ: название отеля, маршрут[hotel_id, poi_id,poi_id, ..., hotel_id], время в пути, расстояние, неучтеные точки")
async def select_optimal_hotel(data: HotelOptimal, hotel:Hotels):
    # return data.time_limit,data.days,data.points_sequence
    return optimal_hotel(data, hotel)

'''



{
  "data": {
    "time_limit": 40,
    "days": 3,
    "points_sequence": [4194,3,4195]
  },
  "hotel": {
    "hotels": [
  {
    "hotel_id": 4,
    "latitude": "55.739982",
    "longitude": "37.62611806",
    "district_id": 4
  },
  {
    "hotel_id": 5,
    "latitude": "55.763842",
    "longitude": "37.614545",
    "district_id": 5
  }
    ]
  }
}




time_limit: int
    days: int
    points_sequence: list[int] = []
    
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

