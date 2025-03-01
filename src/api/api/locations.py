from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from core.database import get_db
from models.location import Location
from schemas.location import LocationSchema, LocationCreate
from schemas.weather import LocationWeather, CurrentWeather
from typing import List


router = APIRouter()

# OpenMeteo API URL
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

@router.get("/locations", response_model=List[LocationWeather])
async def get_locations(db: Session = Depends(get_db)):
    db_locations = db.query(Location).all()
    result = []
    
    async with httpx.AsyncClient() as client:
        for location in db_locations:
            # Fetch current weather data from OpenMeteo
            params = {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "current": "temperature_2m,rain,weather_code",
                "forecast_days": 1
            }
            
            response = await client.get(WEATHER_API_URL, params=params)
            
            if response.status_code == 200:
                weather_data = response.json()
                
                current_weather = CurrentWeather(
                    temperature=weather_data["current"]["temperature_2m"],
                    rainfall=weather_data["current"]["rain"],
                    weather_code=weather_data["current"]["weather_code"]
                )
                
                result.append(
                    LocationWeather(
                        id=location.id,
                        name=location.name,
                        country=location.country,
                        population=location.population,
                        capitalType=location.capitalType,
                        current=current_weather
                    )
                )
            else:
                # If API call fails, add location without weather data
                result.append(
                    LocationWeather(
                        id=location.id,
                        name=location.name,
                        country=location.country,
                        population=location.population,
                        capitalType=location.capitalType,
                        current=CurrentWeather(temperature=0, rainfall=0, weather_code=0)
                    )
                )
    
    return result

@router.post("/locations", response_model=LocationSchema)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = Location(
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude,
        population=location.population,
        capitalType=location.capitalType,
        country=location.country
    )
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/locations/{location_id}", response_model=dict)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    db.delete(db_location)
    db.commit()
    
    return {"message": "Location deleted successfully"}