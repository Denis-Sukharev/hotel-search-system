from pydantic import BaseModel

class Empty():
    pass

#'''SCHEMAS HOTEL'''

class HotelOptimal(BaseModel):
    time_limit: int
    days: int
    points_sequence: list[int] = []


class HotelSchemas(BaseModel):
    hotel_id: int
    name: str
    latitude:str
    longitude: str
    district_id: int

class Hotels(BaseModel):
    hotels: list[HotelSchemas]

class FullInfoHotelPage(BaseModel):
    page: int
    district: list[int] = []
    type: list[str] = []
    rateMin: int
    rateMax: int



class FragmentInfoHotel(BaseModel):
    fragment: str
    district: list[int] = []
    type: list[str] = []
    rateMin: int
    rateMax: int

class IdHotel(BaseModel):
    id_hotel: int

class GetHotelOptimalSchema(BaseModel):
    days: int = 1
    time_limit: int = 7
    district: list[int] = []
    type: list[str] = []
    rateMin: int = 0
    rateMax: int = 10
    points_sequence: list[int] = []


#'''SCHEMAS POI'''

class FullInfoPoiPage(BaseModel):
    page: int
    district: list[int] = []
    type: list[str] = []

class FragmentInfoPoi(BaseModel):
    fragment: str
    district: list[int] = []
    type: list[str] = []

class IdPoi(BaseModel):
    id_poi: int