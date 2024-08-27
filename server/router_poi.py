from typing import Union
from fastapi import APIRouter, HTTPException, status
from database import conn
from schemas import FullInfoPoiPage, IdPoi, FragmentInfoPoi


router = APIRouter(
    tags=['''POI''']
)


@router.post("/poi/all/") # вывод 20 poi для страниц
async def select_poi(data_info: FullInfoPoiPage):
    try:
        with conn:
            with conn.cursor() as cur:          
                cur.execute('''
                        SELECT 
                        COUNT(DISTINCT poi.poi_id)
                        FROM 
                        poi
                        INNER JOIN poi_category ON poi_category.poi_id = poi.poi_id
                        INNER JOIN poi_coordinates ON poi_coordinates.poi_id = poi.poi_id
                        INNER JOIN poi_type ON poi_type.poi_id = poi.poi_id
                        INNER JOIN district ON district.district_id = poi.district_id 
                        WHERE 
                        poi_category.category <> 'Проживание'
                        AND district.district_id = ANY(%s)
                        AND poi_type.type = ANY(%s)
                            ''', (data_info.district, data_info.type)
                            )
                count_poi = cur.fetchall()

                cur.execute('''
                    select
                    distinct 
                    poi.poi_id,
                    poi.name,
                    string_to_array(string_agg(distinct poi_type.type, ','), ',') as type,
                    poi_coordinates.latitude,
                    poi_coordinates.longitude,
                    COALESCE(photo.photo_url, '') AS photo_url
                    from poi
                    inner join poi_category on poi_category.poi_id = poi.poi_id
                    inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                    inner join poi_type on poi_type.poi_id = poi.poi_id
                    inner join district on poi.district_id = district.district_id
                    left join photo on photo.poi_id = poi.poi_id
                    where
                    poi_category.category <> 'Проживание'
                    and district.district_id = ANY(%s)
                    and poi_type.type = ANY(%s)
                    group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude,COALESCE(photo.photo_url, '')
                    order by poi.poi_id
                    offset %s
                    limit 20;
                ''', (data_info.district, data_info.type, (data_info.page*20)))
                data = cur.fetchall()

                result_poi = []
                for item in data:
                    result_poi.append({
                        "id": int(item[0]),
                        "name": str(item[1]),
                        "type": list(item[2]),
                        "latitude": str(item[3]),
                        "longitude": str(item[4]),
                        "photo": str(item[5])
                    })

                result = {
                    "count": count_poi[0][0],
                    "poi": result_poi
                }
                
                return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )


@router.post("/poi/search_name/")# поиск poi по названию
async def select_name_poi(data_info: FragmentInfoPoi):
    try:
        with conn:
            with conn.cursor() as cur:
                # cur.execute("""
                #             SELECT poi.poi_id, poi.name FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category <> 'Проживание' WHERE poi.name ILIKE %s LIMIT 5;
                #             """, ('%' + name_fragment.lower() + '%',))
                cur.execute('''
                    select
                    distinct 
                    poi.poi_id,
                    poi.name,
                    string_to_array(string_agg(distinct poi_type.type, ','), ',') as type,
                    poi_coordinates.latitude,
                    poi_coordinates.longitude,
                    COALESCE(photo.photo_url, '') AS photo_url
                    from poi
                    inner join poi_category on poi_category.poi_id = poi.poi_id
                    inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
                    inner join poi_type on poi_type.poi_id = poi.poi_id
                    inner join district on district.district_id = poi.district_id
                    left join photo on photo.poi_id = poi.poi_id
                    where
                    poi_category.category <> 'Проживание'
                    and district.district_id = ANY(%s)
                    and poi_type.type = ANY(%s)
                    and poi.name ilike %s 
                    group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude, COALESCE(photo.photo_url, '')
                    order by poi.poi_id
                    limit 5;
                ''', ( data_info.district, data_info.type, ('%'+data_info.fragment+'%')))
                data = cur.fetchall()

                result_poi = []
                for item in data:
                    result_poi.append({
                        "id": int(item[0]),
                        "name": str(item[1]),
                        "type": list(item[2]),
                        "latitude": str(item[3]),
                        "longitude": str(item[4]),
                        "photo": str(item[5])
                    })

                result = {
                    "poi": result_poi
                }

                return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )


# @router.post("/poi/search_id/")# поиск poi по id
# async def select_id_poi(id_poi:IdPoi):
#     try:
#         with conn:
#             with conn.cursor() as cur:
#                 cur.execute('''
#                     select
#                     distinct 
#                     poi.poi_id,
#                     poi.name,
#                     string_to_array(string_agg(distinct poi_type.type, ','), ',') as type,
#                     poi_coordinates.latitude,
#                     poi_coordinates.longitude
#                     from poi
#                     inner join poi_category on poi_category.poi_id = poi.poi_id
#                     inner join poi_coordinates on poi_coordinates.poi_id = poi.poi_id
#                     inner join poi_type on poi_type.poi_id = poi.poi_id
#                     inner join district on district.district_id = poi.district_id
#                     where
#                     poi_category.category <> 'Проживание'
#                     and poi.poi_id = %s
#                     group by poi.poi_id, poi_coordinates.latitude, poi_coordinates.longitude
#                     order by poi.poi_id    
#                 ''', (int(id_poi.id_poi),))         

#                 data = cur.fetchall()
#                 result=[]
#                 for item in data:
#                     result.append({
#                         "id": int(item[0]),
#                         "name": str(item[1]),
#                         "type": list(item[2]) ,
#                         "latitude": str(item[3]),
#                         "longitude": str(item[4])
#                     })
#                 return result
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="INTERNAL SERVER ERROR"
#         )
         

# @router.get("/poi/count")# кол-во poi
# async def select_count_poi():
#     with conn:
#         with conn.cursor() as cur:  
#             cur.execute("""
#                         SELECT count(poi.poi_id) FROM poi INNER JOIN poi_category ON poi.poi_id = poi_category.poi_id AND poi_category.category <> 'Проживание';
#                         """)            
#             poi = cur.fetchall()
#             return poi

# class Hotel(BaseModel):
#     name: str
#     address: str
#     rating: int
    
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

