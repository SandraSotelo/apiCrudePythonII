from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal, Base, engine
from models.user import UserModel, UserCreate, User
from routes.items import router as items_router
from typing import List
import json
import logging

logging.basicConfig(level=logging.INFO) # Esto establecerá el nivel de logging a INFO, lo que significa que verás mensajes informativos

app = FastAPI()

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db(): # función que proporciona una sesión de base de datos a los endpoints.
    db = SessionLocal()
    try:
        yield db # para crear contexto: al finalizar la solicitud, la sesión se cierra
    finally:
        db.close()

@app.get('/')
def index():
    return {'Bienvenidos a la API Universidad del Quindío'}

# Endpoint para obtener todos los usuarios
@app.get('/user/', response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    logging.info(f"Visualizando información de los Profesores: {users}")
    for user in users:
        user.semestres = json.loads(user.semestres)
    return users

# Endpoint para crear un nuevo profesor
@app.post('/user/', response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    logging.info(f"Agregando información de los profesores: {user}")
    db_user = UserModel(
        nombreProfesor=user.nombreProfesor,
        asignatura=user.asignatura,
        codigoMateria=user.asignatura,
        semestres=json.dumps(user.semestres)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.semestres = json.loads(db_user.semestres)
    logging.info(f"Profesor Creado: {db_user}")
    return db_user

# Endpoint para actualizar un usuario existente
@app.put('/user/{user_id}', response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")    
    db_user.nombreProfesor= user.nombreProfesor
    db_user.asignatura= user.asignatura
    db_user.codigoMateria= user.codigoMateria
    db_user.semestres = json.dumps(user.semestres)    
    db.commit()
    db.refresh(db_user)    
    db_user.semestres = json.loads(db_user.semestres)
    return db_user

# Endpoint para borrar un usuario
@app.delete('/user/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="El profesor no fue encontrado")
    db.delete(db_user)
    db.commit()
    return db_user

# Incluye el router de items
app.include_router(items_router)

@app.get("/favicon.ico")
async def favicon():
    return {}