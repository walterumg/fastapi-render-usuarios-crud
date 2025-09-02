from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from .db import Base, engine, get_db
from .models import Usuario
from .schemas import UsuarioCreate, UsuarioOut
from datetime import datetime

app = FastAPI(title="API Usuarios", version="1.0.0")

Base.metadata.create_all(bind=engine)

@app.get("/api/saludo")
def saludo():
    return {"mensaje": "Hola mundo"}

@app.get("/api/now")
def now():
    return {"now": datetime.utcnow().isoformat() + "Z"}

@app.get("/api/usuarios", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).order_by(Usuario.id_usuario).all()

@app.post("/api/usuarios", response_model=UsuarioOut, status_code=201)
def crear_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.correo == payload.correo).first():
        raise HTTPException(status_code=409, detail="Correo ya registrado")

    hashed = bcrypt.hash(payload.password)
    u = Usuario(nombre=payload.nombre, correo=payload.correo, password=hashed)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@app.put("/api/usuarios/{id_usuario}", response_model=UsuarioOut)
def actualizar_usuario(id_usuario: int, payload: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if db.query(Usuario).filter(Usuario.correo == payload.correo, Usuario.id_usuario != id_usuario).first():
        raise HTTPException(status_code=409, detail="Correo ya registrado")

    usuario.nombre = payload.nombre
    usuario.correo = payload.correo
    usuario.password = bcrypt.hash(payload.password)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.delete("/api/usuarios/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return
