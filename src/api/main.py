from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.locations import router as locations_router
from api.models import Base
from api.core.database import engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(locations_router, prefix="/locations", tags=["locations"])

@app.get("/")
def read_root():
    return {"message": "Weather Dashboard API"}