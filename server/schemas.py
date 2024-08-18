from pydantic import BaseModel


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


