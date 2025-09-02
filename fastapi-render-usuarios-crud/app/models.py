from sqlalchemy import Column, Integer, String, DateTime, func
from .db import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100), nullable=False)
    correo     = Column(String(150), unique=True, nullable=False, index=True)
    password   = Column(String(100), nullable=False)
    fecha_reg  = Column(DateTime, server_default=func.now())
