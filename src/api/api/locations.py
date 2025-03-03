from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
import datetime


from api.api.schemas import LocationCreate, Location as LocationSchema, LocationWithWeather, Forecast, ForecastDay, WeatherData
from api.core.database import get_db
from api.models.location import Location
router = APIRouter()

async def fetch_weather_data(lat: float, lon: float):
    """Fetch current weather data from OpenMeteo API"""
    async with httpx.AsyncClient() as client:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,rain,weather_code",
            "timezone": "auto"
        }
        response = await client.get(url, params=params)
        data = response.json()
        
        return WeatherData(
            temperature=data["current"]["temperature_2m"],
            rainfall=data["current"]["rain"],
            wmo_code=data["current"]["weather_code"]
        )

async def fetch_forecast_data(lat: float, lon: float):
    """Fetch 7-day forecast data from OpenMeteo API"""
    today = datetime.datetime.now().date()
    end_date = today + datetime.timedelta(days=6)
    
    async with httpx.AsyncClient() as client:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,rain_sum,weather_code",
            "timezone": "auto",
            "start_date": today.isoformat(),
            "end_date": end_date.isoformat()
        }
        response = await client.get(url, params=params)
        data = response.json()
        
        days = []
        for i in range(len(data["daily"]["time"])):
            days.append(ForecastDay(
                date=data["daily"]["time"][i],
                temperature=data["daily"]["temperature_2m_max"][i],
                rainfall=data["daily"]["rain_sum"][i],
                wmo_code=data["daily"]["weather_code"][i]
            ))
        
        return days

@router.get("/", response_model=List[LocationWithWeather])
async def get_locations(db: Session = Depends(get_db)):
    """Get all locations with their current weather"""
    locations = db.query(Location).all()
    result = []
    
    for location in locations:
        weather = await fetch_weather_data(location.latitude, location.longitude)
        result.append(LocationWithWeather(
            id=location.id,
            name=location.name,
            latitude=location.latitude,
            longitude=location.longitude,
            weather=weather
        ))
    
    return result

@router.post("/", response_model=LocationSchema)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    """Add a new location"""
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Delete a location by ID"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    db.delete(location)
    db.commit()
    return {"message": "Location deleted successfully"}

@router.get("/forecast/{location_id}", response_model=Forecast)
async def get_forecast(location_id: int, db: Session = Depends(get_db)):
    """Get 7-day forecast for a location"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    forecast_days = await fetch_forecast_data(location.latitude, location.longitude)
    
    return Forecast(
        location_id=location.id,
        location_name=location.name,
        days=forecast_days
    )