from finding_ways.start import optimal_hotel
from typing import Union
from fastapi import APIRouter, HTTPException, status
from database import conn
from schemas import Empty, HotelOptimal, Hotels, FullInfoHotelPage, FragmentInfoHotel, IdHotel, GetHotelOptimalSchema


router = APIRouter(
    tags=['HOTEL']
)
   

@router.post("/hotel/all/")# вывод 20 hotel для страниц
async def select_hotel(data_info: FullInfoHotelPage):
    try:
        with conn:
            with conn.cursor() as cur:
                # cur.execute('''
                #     select
                #     distinct
                #     count(*)
                #     from poi
                #     inner join poi_category on poi_category.poi_id = poi.poi_id
                #     inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                #     inner join poi_type on poi_type.poi_id = poi_type.poi_id
                #     inner join district on district.district_id = poi.district_id 
                #     inner join hotel_rating on hotel_rating.poi_id = poi.poi_id 
                #     where
                #     poi_category.category = 'Проживание'
                #     and district.district_id = ANY(%s)
                #     and poi_type.type = ANY(%s)
                #     and hotel_rating.rating between %s and %s
                #     group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating;
                #             ''', (data_info.district, data_info.type, int(data_info.rateMin), int(data_info.rateMax))
                #             )
                cur.execute('''
                        SELECT 
                        COUNT(DISTINCT poi.poi_id)
                        FROM 
                        poi
                        INNER JOIN poi_category ON poi_category.poi_id = poi.poi_id
                        INNER JOIN poi_coordinates ON poi_coordinates.poi_id = poi.poi_id
                        INNER JOIN poi_type ON poi_type.poi_id = poi.poi_id
                        INNER JOIN district ON district.district_id = poi.district_id 
                        INNER JOIN hotel_rating ON hotel_rating.poi_id = poi.poi_id 
                        WHERE 
                        poi_category.category = 'Проживание'
                        AND district.district_id = ANY(%s)
                        AND poi_type.type = ANY(%s)
                        AND hotel_rating.rating BETWEEN %s AND %s;
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
                    poi_coordinates.longitude,
                    COALESCE(photo.photo_url, '') AS photo_url      
                    from poi
                    inner join poi_category on poi_category.poi_id = poi.poi_id
                    inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                    inner join poi_type on poi_type.poi_id = poi.poi_id
                    inner join district on poi.district_id = district.district_id
                    inner join hotel_rating on hotel_rating.poi_id = poi.poi_id 
                    inner join photo on photo.poi_id = poi.poi_id
                    where
                    poi_category.category = 'Проживание'
                    and district.district_id = ANY(%s)
                    and poi_type.type = ANY(%s)
                    and hotel_rating.rating >= %s
                    and hotel_rating.rating <= %s
                    group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating, COALESCE(photo.photo_url, '')
                    order by poi.poi_id
                    offset %s
                    limit 20;
                ''', (data_info.district, data_info.type, int(data_info.rateMin), int(data_info.rateMax), (data_info.page*20)))
                data = cur.fetchall()

                result_hotels = []
                for item in data:
                    result_hotels.append({
                        "id": int(item[0]),
                        "name": str(item[1]),
                        "type": list(item[2]),
                        "rating": float(item[3]),
                        "latitude": str(item[4]),
                        "longitude": str(item[5]),
                        "photo": str(item[6])
                    })

                result = {
                    "count": count_hotel[0][0],
                    "hotels": result_hotels
                }

                return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )

@router.post("/hotel/search_name/")# поиск hotel по name
async def select_name_hotel(data_info: FragmentInfoHotel):
    try: 
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
                    poi_coordinates.longitude,
                    COALESCE(photo.photo_url, '') AS photo_url
                    from poi
                    inner join poi_category on poi_category.poi_id = poi.poi_id
                    inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                    inner join poi_type on poi_type.poi_id = poi.poi_id
                    inner join district on district.district_id = poi.district_id
                    inner join hotel_rating on hotel_rating.poi_id = poi.poi_id
                    inner join photo on photo.poi_id = poi.poi_id                    
                    where
                    poi_category.category = 'Проживание'
                    and district.district_id = ANY(%s)
                    and poi_type.type = ANY(%s)
                    and hotel_rating.rating >= %s
                    and hotel_rating.rating <= %s
                    and poi.name ilike %s
                    group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating, COALESCE(photo.photo_url, '')
                    order by poi.poi_id
                    limit 5;
                ''',(data_info.district, data_info.type, int(data_info.rateMin), int(data_info.rateMax), ('%'+data_info.fragment+'%')))
                data = cur.fetchall()
                
                result_hotels = []
                for item in data:
                    result_hotels.append({
                        "id": int(item[0]),
                        "name": str(item[1]),
                        "type": list(item[2]),
                        "rating": float(item[3]),
                        "latitude": str(item[4]),
                        "longitude": str(item[5]),
                        "photo": str(item[6])

                    })
                    
                result = {
                    "hotels": result_hotels
                }
                
                return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    


        

# @router.post("/hotel/search_id/")# поиск hotel по id
# async def select_id_hotel(id_poi: IdHotel):
#     try:
#         with conn:
#             with conn.cursor() as cur:  
#                 # cur.execute("""
#                 #             SELECT * FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category = 'Проживание' WHERE poi.poi_id = %s;
#                 #             """, (id_poi,))   
#                 cur.execute('''
#                     select
#                     distinct 
#                     poi.poi_id,
#                     poi.name,
#                     string_to_array(string_agg(distinct poi_type.type, ','), ',') as type,
#                     hotel_rating.rating,
#                     poi_coordinates.latitude,
#                     poi_coordinates.longitude
#                     from poi
#                     inner join poi_category on poi_category.poi_id = poi.poi_id
#                     inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
#                     inner join poi_type on poi_type.poi_id = poi.poi_id
#                     inner join district on district.district_id = poi.district_id
#                     inner join hotel_rating on hotel_rating.poi_id = poi.poi_id
#                     where
#                     poi_category.category = 'Проживание'
#                     and poi.poi_id = %s
#                     group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating
#                     order by poi.poi_id    
#                 ''', (id_poi.id_hotel,))         

#                 data = cur.fetchall()
#                 result=[]
#                 for item in data:
#                     result.append({
#                         "id": int(item[0]),
#                         "name": str(item[1]),
#                         "type": str(item[2]),
#                         "rating": float(item[3]),
#                         "latitude": str(item[4]),
#                         "longitude": str(item[5])
#                     })
#                 return result
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="INTERNAL SERVER ERROR"
#         )


# @router.get("/hotel/count")# кол-во hotel
# async def select_count_hotel():
#     with conn:
#         with conn.cursor() as cur:  
#             cur.execute("""
#                         SELECT count(poi.poi_id) FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category = 'Проживание';
#                         """)            
#             hotel = cur.fetchall()
#             return hotel
        

@router.post("/route/optimal/")
async def select_optimal_route(data: HotelOptimal, hotel:Hotels):
    try:
        # return data.time_limit,data.days,data.points_sequence
        return optimal_hotel(data, hotel)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )



@router.post("/hotel/optimal/")
async def select_optimal_hotel(data: GetHotelOptimalSchema):
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('''
                    select
                    distinct 
                    poi.poi_id,
                    poi.name,
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
                    and hotel_rating.rating >= %s
                    and hotel_rating.rating <= %s
                    group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating
                    order by poi.poi_id;
                ''', (data.district, data.type, int(data.rateMin), int(data.rateMax)))
                hotels_data = cur.fetchall()

                hotels = []
                for item in hotels_data:
                    hotels.append({
                        "hotel_id": int(item[0]),
                        "name": str(item[1]),
                        "latitude": str(item[2]),
                        "longitude": str(item[3]),
                        "district_id": 0
                    })

                data_ = HotelOptimal(time_limit=int(data.time_limit), days=int(data.days), points_sequence=data.points_sequence)

                hotels_ = Hotels(hotels=hotels)


                optimal_hotels = []
                tmp_optimal_hotels = optimal_hotel(data_, hotels_)
                for item in tmp_optimal_hotels:
                    optimal_hotels.append(int(item['route'][0]))

                cur.execute('''
                    select
                    distinct 
                    poi.poi_id,
                    poi.name,
                    string_to_array(string_agg(distinct poi_type.type, ','), ',') as type,
                    hotel_rating.rating,
                    poi_coordinates.latitude,
                    poi_coordinates.longitude,
                    COALESCE(photo.photo_url, '') AS photo_url
                    from poi
                    inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                    inner join poi_type on poi_type.poi_id = poi.poi_id
                    inner join district on district.district_id = poi.district_id
                    inner join hotel_rating on hotel_rating.poi_id = poi.poi_id
                    inner join photo on photo.poi_id = poi.poi_id                    
                    where
                    poi.poi_id = ANY(%s)
                    group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, hotel_rating.rating, COALESCE(photo.photo_url, '');
                ''',(optimal_hotels,))
                optimal_hotels_data = cur.fetchall()

                result_hotels = []
                for item in optimal_hotels_data:
                    result_hotels.append({
                        "id": int(item[0]),
                        "name": str(item[1]),
                        "type": list(item[2]),
                        "rating": float(item[3]),
                        "latitude": str(item[4]),
                        "longitude": str(item[5]),
                        "photo": str(item[6])
                    })
                    
                result = {
                    "hotels": result_hotels
                }
                
                return result
    except Exception as e:
        print (e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    


# def getPoiData(poiArray):
#     res: list[{}]   
#     for poiId in poiArray:      
#         (```
#         select p.name, pc.latitude, pc.longitude
#         from poi as p
#         inner join poi_coordinates as pc on pc.poi_id = p.poi_id
#         where p.poi_id = %s;
#         ```, {poiId})     
#         res.append({
#             "name": sql.name,
#             "x", sql.x,
#             "y": sql.y
#         })   
#     return res
# {
#   "data": {
#     "time_limit": 40,
#     "days": 3,
#     "points_sequence": [4194,3,4195]
#   },
#   "hotel": {
#     "hotels": [
#   {
#     "hotel_id": 4,
#     "name":"108 Minutes",
#     "latitude": "55.739982",
#     "longitude": "37.62611806",
#     "district_id": 4
#   },
#   {
#     "hotel_id": 5,
#     "name":"17/3 Capsule hotel and lounge",
#     "latitude": "55.763842",
#     "longitude": "37.614545",
#     "district_id": 5
#   }
#     ]
#   }
# }




# time_limit: int
#     days: int
#     points_sequence: list[int] = []
    
# @router.get("/hotels/{hotel_id}")
# async def read_hotel(hotel_id: int):
#     return {"name": "Hotel 1", "address": "Address 1", "rating": 5}

# @router.post("/hotels/")
# async def create_hotel(hotel: Hotel):
#     return hotel

# @router.put("/hotels/{hotel_id}")
# async def update_hotel(hotel_id: int, hotel: Hotel):
#     return hotel

# @router.delete("/hotels/{hotel_id}")
# async def delete_hotel(hotel_id: int):
#     return {"message": "Hotel deleted"}