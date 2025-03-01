from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from core.database import get_db
from models.location import Location
from schemas.weather import DetailedForecast, DailyForecast

router = APIRouter()

# OpenMeteo API URL
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

@router.get("/forecast/{location_id}", response_model=DetailedForecast)
async def get_forecast(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Fetch 7-day forecast from OpenMeteo
    params = {
        "latitude": db_location.latitude,
        "longitude": db_location.longitude,
        "daily": "temperature_2m_max,temperature_2m_min,rain_sum,weather_code",
        "forecast_days": 7,
        "timezone": "auto"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_API_URL, params=params)
        
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch weather forecast")
        
        forecast_data = response.json()
        
        daily_forecasts = []
        for i in range(len(forecast_data["daily"]["time"])):
            daily_forecasts.append(
                DailyForecast(
                    date=forecast_data["daily"]["time"][i],
                    temperature_max=forecast_data["daily"]["temperature_2m_max"][i],
                    temperature_min=forecast_data["daily"]["temperature_2m_min"][i],
                    rainfall_sum=forecast_data["daily"]["rain_sum"][i],
                    weather_code=forecast_data["daily"]["weather_code"][i]
                )
            )
        
        return DetailedForecast(
            location_name=db_location.name,
            daily=daily_forecasts
        )