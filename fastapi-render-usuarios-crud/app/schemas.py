from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

class UsuarioOut(BaseModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    class Config:
        from_attributes = True
