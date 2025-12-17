from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.models.user_model import UserIn, UserOut
from app.repositories.user_repository import UsuarioRepository
from app.services.auth_service import AuthService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

repo = UsuarioRepository()
auth_service = AuthService()

@router.post("/", response_model=UserOut)
async def crear_usuario(user: UserIn, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await auth_service.registrar(
        db, user.nombre, user.email, user.password, user.rol
    )

@router.get("/", response_model=list[UserOut])
async def listar_usuarios(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await repo.obtener_todos(db)

@router.get("/{user_id}", response_model=UserOut)
async def obtener_usuario(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    usuario = await repo.obtener_por_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{user_id}", response_model=UserOut)
async def actualizar_usuario(user_id: str, user: UserIn, db: AsyncIOMotorDatabase = Depends(get_db)):
    usuario = await repo.obtener_por_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = {
        "nombre": user.nombre,
        "rol": user.rol
    }
    
    updated_user = await repo.actualizar(db, user_id, update_data)
    return updated_user

@router.delete("/{user_id}")
async def eliminar_usuario(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    usuario = await repo.obtener_por_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    await repo.eliminar(db, user_id)
    return {"mensaje": "Usuario eliminado correctamente"}
