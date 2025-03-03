from pydantic import BaseModel
from typing import List, Optional

class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True

class WeatherData(BaseModel):
    temperature: float
    rainfall: float
    wmo_code: int

class LocationWithWeather(Location):
    weather: WeatherData

class ForecastDay(BaseModel):
    date: str
    temperature: float
    rainfall: float
    wmo_code: int

class Forecast(BaseModel):
    location_id: int
    location_name: str
    days: List[ForecastDay]