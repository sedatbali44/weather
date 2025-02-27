# main.py
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import httpx
import os
import csv
import io
from typing import List, Optional
from pydantic import BaseModel

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/weather_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class LocationResponse(LocationBase):
    id: int
    
    class Config:
        orm_mode = True

class WeatherData(BaseModel):
    temperature: float
    rainfall: float
    weather_code: int

class LocationWeather(LocationResponse):
    weather: WeatherData

class ForecastDay(BaseModel):
    date: str
    temperature: float
    rainfall: float
    weather_code: int

class ForecastResponse(BaseModel):
    location: LocationResponse
    forecast: List[ForecastDay]

class AvailableLocation(BaseModel):
    name: str
    latitude: float
    longitude: float

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Helper function to fetch current weather data
async def fetch_weather(lat: float, lon: float):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,rain,weather_code",
            },
        )
        data = response.json()
        return WeatherData(
            temperature=data["current"]["temperature_2m"],
            rainfall=data["current"]["rain"],
            weather_code=data["current"]["weather_code"]
        )

# Helper function to fetch forecast data
async def fetch_forecast(lat: float, lon: float):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,rain_sum,weather_code",
                "timezone": "auto",
                "forecast_days": 7,
            },
        )
        data = response.json()
        forecast = []
        
        for i in range(len(data["daily"]["time"])):
            forecast.append(
                ForecastDay(
                    date=data["daily"]["time"][i],
                    temperature=data["daily"]["temperature_2m_max"][i],
                    rainfall=data["daily"]["rain_sum"][i],
                    weather_code=data["daily"]["weather_code"][i]
                )
            )
        
        return forecast

# Global variable to store cities data
CITIES_DATA = []

# Function to load cities from CSV file
def load_cities_from_csv(file_path=None):
    cities = []
    
    # Try loading from provided file path first (development mode)
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # Adapt field names to match your CSV structure
                    city_name = row.get("capital") or row.get("city_name") or row.get("name")
                    lat = row.get("lat") or row.get("latitude") 
                    lng = row.get("lng") or row.get("longitude") or row.get("long")
                    
                    if city_name and lat and lng:
                        try:
                            cities.append({
                                "name": city_name,
                                "latitude": float(lat),
                                "longitude": float(lng)
                            })
                        except (ValueError, TypeError):
                            pass
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
    
    # If no cities loaded yet, try container path (production mode)
    if not cities:
        container_path = os.path.join(os.path.dirname(__file__), "cities.csv")
        if os.path.exists(container_path):
            try:
                with open(container_path, "r", encoding="utf-8") as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        # Using standard field names from GitHub example
                        try:
                            cities.append({
                                "name": row["city_ascii"],
                                "latitude": float(row["lat"]),
                                "longitude": float(row["lng"])
                            })
                        except (KeyError, ValueError, TypeError):
                            pass
            except Exception as e:
                print(f"Error reading container CSV file: {str(e)}")
    
    # If still no cities, provide fallback data
    if not cities:
        cities = [
            {"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
            {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
            {"name": "Tokyo", "latitude": 35.6762, "longitude": 139.6503},
            {"name": "Sydney", "latitude": -33.8688, "longitude": 151.2093},
            {"name": "Paris", "latitude": 48.8566, "longitude": 2.3522}
        ]
    
    print(f"Successfully loaded {len(cities)} cities")
    return cities


CITIES_CSV_PATH = "C:\Users\sedat\Downloads\country-capitals\country-capital-lat-long-population.csv"

@app.on_event("startup")
def startup_event():
    global CITIES_DATA
    CITIES_DATA = load_cities_from_csv(CITIES_CSV_PATH)


# Routes
@app.get("/")
def root():
    return {"message": "Weather API is running"}

@app.get("/locations", response_model=List[LocationWeather])
async def get_locations(db: Session = Depends(get_db)):
    locations = db.query(Location).all()
    result = []
    
    for location in locations:
        try:
            weather = await fetch_weather(location.latitude, location.longitude)
            result.append(
                LocationWeather(
                    id=location.id,
                    name=location.name,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    weather=weather
                )
            )
        except Exception as e:
            # Handle API errors gracefully
            print(f"Error fetching weather for {location.name}: {str(e)}")
            result.append(
                LocationWeather(
                    id=location.id,
                    name=location.name,
                    latitude=location.latitude,
                    longitude=location.longitude,
                    weather=WeatherData(temperature=0, rainfall=0, weather_code=0)
                )
            )
    
    return result

@app.post("/locations", response_model=LocationResponse, status_code=201)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    # Check if location already exists
    existing_location = db.query(Location).filter(
        Location.name == location.name
    ).first()
    
    if existing_location:
        raise HTTPException(status_code=400, detail="Location already exists")
    
    # Create new location
    db_location = Location(
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude
    )
    
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    return db_location

@app.delete("/locations/{location_id}", status_code=204)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    db.delete(location)
    db.commit()
    
    return None

@app.get("/forecast/{location_id}", response_model=ForecastResponse)
async def get_forecast(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == location_id).first()
    
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    try:
        forecast_data = await fetch_forecast(location.latitude, location.longitude)
        
        return ForecastResponse(
            location=LocationResponse(
                id=location.id,
                name=location.name,
                latitude=location.latitude,
                longitude=location.longitude
            ),
            forecast=forecast_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching forecast: {str(e)}")

@app.get("/available-locations", response_model=List[AvailableLocation])
def get_available_locations():
    global CITIES_DATA
    return [AvailableLocation(name=city["name"], latitude=city["latitude"], longitude=city["longitude"]) for city in CITIES_DATA]

@app.post("/upload-cities-csv")
async def upload_cities_csv(file: UploadFile = File(...)):
    global CITIES_DATA
    
    try:
        contents = await file.read()
        buffer = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(buffer)
        cities = []
        
        for row in csv_reader:
            # Adapt these field names based on your CSV structure
            city_name = row.get("capital") or row.get("city_name") or row.get("name")
            lat = row.get("lat") or row.get("latitude")
            lng = row.get("lng") or row.get("longitude") or row.get("long")
            
            if city_name and lat and lng:
                try:
                    cities.append({
                        "name": city_name,
                        "latitude": float(lat),
                        "longitude": float(lng)
                    })
                except (ValueError, TypeError):
                    pass
        
        if cities:
            CITIES_DATA = cities
            return {"message": f"Successfully loaded {len(cities)} cities from uploaded CSV"}
        else:
            return {"message": "No valid cities found in the uploaded CSV"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


#docker run -p 8000:8000 weather-api
@app.post("/load-initial-data", status_code=201)
def load_initial_data(db: Session = Depends(get_db)):
    global CITIES_DATA
    if not CITIES_DATA:
        raise HTTPException(status_code=500, detail="No city data available")

    count = 0
    cities_to_load = CITIES_DATA[:20]  # Limit for testing

    for city in cities_to_load:
        existing_location = db.query(Location).filter(Location.name == city["name"]).first()

        if not existing_location:
            db_location = Location(
                name=city["name"],
                latitude=city["latitude"],
                longitude=city["longitude"]
            )
            db.add(db_location)
            count += 1

    db.commit()
    return {"message": f"Initial data loaded successfully: {count} locations added"}

    global CITIES_DATA
    count = 0

    # Limit to first 20 cities for demo to avoid overloading the database
    cities_to_load = CITIES_DATA[:20]

    for city in cities_to_load:
        # Check if location already exists
        existing_location = db.query(Location).filter(
            Location.name == city["name"]
        ).first()

        if not existing_location:
            # Create new location
            db_location = Location(
                name=city["name"],
                latitude=city["latitude"],
                longitude=city["longitude"]
            )

            db.add(db_location)
            count += 1

    db.commit()

    return {"message": f"Initial data loaded successfully: {count} locations added"}

    global CITIES_DATA
    count = 0
    
    # Limit to first 20 cities for demo to avoid overloading the database
    cities_to_load = CITIES_DATA[:20]
    
    for city in cities_to_load:
        # Check if location already exists
        existing_location = db.query(Location).filter(
            Location.name == city["name"]
        ).first()
        
        if not existing_location:
            # Create new location
            db_location = Location(
                name=city["name"],
                latitude=city["latitude"],
                longitude=city["longitude"]
            )
            
            db.add(db_location)
            count += 1
    
    db.commit()
    
    return {"message": f"Initial data loaded successfully: {count} locations added"}

# For development/testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)