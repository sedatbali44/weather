from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine
from api.locations import router as locations_router
from models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(locations_router, prefix="/locations", tags=["locations"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# Include routers
app.include_router(locations_router, prefix="/locations", tags=["locations"])

@app.get("/")
def read_root():
    return {"message": "Weather Dashboard API"}