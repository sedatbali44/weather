# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import locations, weather
from api.core.database import engine
from api.models import Base

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
app.include_router(locations.router, tags=["Locations"])
app.include_router(weather.router, tags=["Weather"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Weather Dashboard API"}