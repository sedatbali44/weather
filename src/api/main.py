from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api.locations import router as locations_router
from api.api.weather import router as weather_router
from api.models import Base
from api.core.database import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Dashboard API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(locations_router, tags=["Locations"])
app.include_router(weather_router, tags=["Weather"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Weather Dashboard API"}