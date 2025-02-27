from pydantic import BaseModel
from typing import List, Optional

class CurrentWeather(BaseModel):
    temperature: float
    rainfall: float
    weather_code: int

class DailyForecast(BaseModel):
    date: str
    temperature_max: float
    temperature_min: float
    rainfall_sum: float
    weather_code: int

class LocationWeather(BaseModel):
    id: int
    name: str
    current: CurrentWeather

class DetailedForecast(BaseModel):
    location_name: str
    daily: List[DailyForecast]