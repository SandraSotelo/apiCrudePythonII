from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import json
from models.database import engine, Base
Base.metadata.create_all(bind=engine)

# Modelo de SQLAlchemy
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nombreProfesor = Column(String, index=True)
    asignatura = Column(String, index=True)
    codigoMateria = Column(String, index=True)
    semestres = Column(Text)
   
# Esquema Pydantic para crear un usuario
class UserCreate(BaseModel):
    nombreProfesor: str
    asignatura: str
    codigoMateria: str
    semestres: List[int] = []  

# Esquema Pydantic para la respuesta de usuario
class User(BaseModel):
    id: int
    nombreProfesor: str
    asignatura: str
    codigoMateria: str
    semestres: List[int] = []  

    class Config:
        from_attributes = True  # Actualizado para Pydantic v2
        
# Funciones para manejar el almacenamiento
def serialize_values(values):
    return json.dumps(values)  # Serializa la lista a JSON

def deserialize_values(values):
    return json.loads(values)  # Deserializa el JSON a lista

