# import sys
# sys.path.append('../finding_ways/')
from finding_ways.start import optimal_hotel

from typing import Union
from fastapi import APIRouter
from server.database import conn
from server.schemas import HotelOptimal, Hotels, FullInfoHotelPage, FragmentInfoHotel, IdHotel
router = APIRouter(
    tags=['''HOTEL''']
)
   
@router.post("/hotel/all/")# вывод 20 hotel для страниц
async def select_hotel(data_info: FullInfoHotelPage):
    with conn:
        with conn.cursor() as cur:
            cur.execute('''
                select
                distinct 
                count(poi.poi_id)
                from poi
                inner join poi_category on poi_category.poi_id = poi.poi_id
                inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                inner join poi_type on poi_type.poi_id = poi_type.poi_id
                inner join district on district.district_id = poi.district_id 
                inner join hotel_rating on hotel_rating.poi_id = poi.poi_id 
                where
                poi_category.category = 'Проживание'
                and district.district_id = ANY(%s)
                and poi_type.type = ANY(%s)
                and hotel_rating.rating between %s and %s
                group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating
                        ''', (data_info.district, data_info.type, int(data_info.rateMin), int(data_info.rateMax))
                        )
            count_hotel = cur.fetchall()
            cur.execute('''
                select
                distinct 
                poi.poi_id,
                poi.name,
                string_to_array(string_agg(distinct poi_type.type, ','), ',') as type,
                hotel_rating.rating,
                poi_coordinates.latitude,
                poi_coordinates.longitude
                from poi
                inner join poi_category on poi_category.poi_id = poi.poi_id
                inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                inner join poi_type on poi_type.poi_id = poi.poi_id
                inner join district on poi.district_id = district.district_id
                inner join hotel_rating on hotel_rating.poi_id = poi.poi_id 
                where
                poi_category.category = 'Проживание'
                and district.district_id = ANY(%s)
                and poi_type.type = ANY(%s)
                and hotel_rating.rating between %s and %s
                group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating
                order by poi.poi_id
                offset %s
                limit 20;
            ''', (data_info.district, data_info.type, int(data_info.rateMin), int(data_info.rateMax), (data_info.page*20)))
            data = cur.fetchall()
            result = []
            result.append({
                "count": count_hotel[0][0]
                })
            for item in data:
                result.append({
                    "id": int(item[0]),
                    "name": str(item[1]),
                    "type": list(item[2]),
                    "rating": float(item[3]),
                    "latitude": str(item[4]),
                    "longitude": str(item[5])
                })
            return result

@router.post("/hotel/search_name/")# поиск hotel по name
async def select_name_hotel(data_info: FragmentInfoHotel):
    with conn:
        with conn.cursor() as cur:  
            cur.execute('''
                select
                distinct 
                poi.poi_id,
                poi.name,
                string_to_array(string_agg(distinct poi_type.type, ','), ',') as type,
                hotel_rating.rating,
                poi_coordinates.latitude,
                poi_coordinates.longitude
                from poi
                inner join poi_category on poi_category.poi_id = poi.poi_id
                inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                inner join poi_type on poi_type.poi_id = poi.poi_id
                inner join district on district.district_id = poi.district_id
                inner join hotel_rating on hotel_rating.poi_id = poi.poi_id
                where
                poi_category.category = 'Проживание'
                and district.district_id = ANY(%s)
                and poi_type.type = ANY(%s)
                and hotel_rating.rating between %s and %s
                and poi.name ilike %s
                group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating
                order by poi.poi_id
                limit 5;
            ''',(data_info.district, data_info.type, int(data_info.rateMin), int(data_info.rateMax), ('%'+data_info.fragment+'%')))
            data = cur.fetchall()
            result=[]
            for item in data:
                result.append({
                    "id": int(item[0]),
                    "name": str(item[1]),
                    "type": str(item[2]),
                    "rating": float(item[3]),
                    "latitude": str(item[4]),
                    "longitude": str(item[5])
                })
            return result 

@router.post("/hotel/search_id/")# поиск hotel по id
async def select_id_hotel(id_poi: IdHotel):
    with conn:
        with conn.cursor() as cur:  
            # cur.execute("""
            #             SELECT * FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category = 'Проживание' WHERE poi.poi_id = %s;
            #             """, (id_poi,))   
            cur.execute('''
                select
                distinct 
                poi.poi_id,
                poi.name,
                string_to_array(string_agg(distinct poi_type.type, ','), ',') as type,
                hotel_rating.rating,
                poi_coordinates.latitude,
                poi_coordinates.longitude
                from poi
                inner join poi_category on poi_category.poi_id = poi.poi_id
                inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                inner join poi_type on poi_type.poi_id = poi.poi_id
                inner join district on district.district_id = poi.district_id
                inner join hotel_rating on hotel_rating.poi_id = poi.poi_id
                where
                poi_category.category = 'Проживание'
                and poi.poi_id = %s
                group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating
                order by poi.poi_id    
            ''', (id_poi.id_hotel,))         

            data = cur.fetchall()
            result=[]
            for item in data:
                result.append({
                    "id": int(item[0]),
                    "name": str(item[1]),
                    "type": str(item[2]),
                    "rating": float(item[3]),
                    "latitude": str(item[4]),
                    "longitude": str(item[5])
                })
            return result


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

def getPoiData(poiArray):
    res: list[{}]
    
    for poiId in poiArray:
        
        (```
        select p.name, pc.latitude, pc.longitude
        from poi as p
        inner join poi_coordinates as pc on pc.poi_id = p.poi_id
        where p.poi_id = %s;
        ```, {poiId})
        
        res.append({
            "name": sql.name,
            "x", sql.x,
            "y": sql.y
        })
    
    return res

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
    "name":"108 Minutes",
    "latitude": "55.739982",
    "longitude": "37.62611806",
    "district_id": 4
  },
  {
    "hotel_id": 5,
    "name":"17/3 Capsule hotel and lounge",
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

