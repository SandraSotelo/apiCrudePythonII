from fastapi import APIRouter
from pydantic import BaseModel, validator
from typing import Optional

router = APIRouter()

class Item(BaseModel):
    nombreProfesor: str
    price: float
    is_offer: Optional[bool] = False  # Cambiado a Optional
    #is_offer: bool = None

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

@router.post("/items/")
def create_item(item: Item):
    return {"item": item}

@router.get("/items/")
def get_items():
    return {"message": "Aquí puedes obtener los items."}
