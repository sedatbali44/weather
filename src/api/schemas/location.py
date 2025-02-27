from pydantic import BaseModel

class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class LocationSchema(LocationBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True