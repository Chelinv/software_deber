# app/api/endpoints/user_controller.py
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.repositories.user_repository import UsuarioRepository
from app.models.usuario_models import UsuarioCreate, UsuarioUpdate, UsuarioOut
from typing import List

# Inicia la instancia del Router/Controlador
router = APIRouter()
usuario_repo = UsuarioRepository()

@router.post("/", response_model=UsuarioOut)
async def crear_usuario(usuario: UsuarioCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.
    """
    try:
        usuario_dict = usuario.model_dump()
        nuevo_usuario = await usuario_repo.crear(db, usuario_dict)
        return UsuarioOut(**nuevo_usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UsuarioOut])
async def listar_usuarios(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Obtiene la lista de todos los usuarios.
    """
    try:
        usuarios = await usuario_repo.obtener_todos(db)
        return [UsuarioOut(**u) for u in usuarios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=UsuarioOut)
async def obtener_usuario(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Obtiene la información de un usuario por su ID.
    """
    usuario = await usuario_repo.obtener_por_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UsuarioOut(**usuario)

@router.put("/{user_id}", response_model=UsuarioOut)
async def actualizar_usuario(user_id: str, usuario: UsuarioUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Actualiza la información de un usuario existente.
    """
    try:
        # Preparar datos para actualización (solo campos no nulos)
        update_data = {k: v for k, v in usuario.model_dump(exclude_unset=True).items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        # Si se está actualizando la contraseña, hashearla
        if "password" in update_data and update_data["password"]:
            from app.services.auth_service import AuthService
            auth_service = AuthService()
            update_data["password"] = auth_service.hash_password(update_data["password"])
        
        # Actualizar usando el repositorio
        usuario_actualizado = await usuario_repo.actualizar(db, user_id, update_data)
        
        if not usuario_actualizado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return UsuarioOut(**usuario_actualizado)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
async def eliminar_usuario(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Elimina un usuario del sistema.
    """
    try:
        # Verificar que el usuario existe
        usuario = await usuario_repo.obtener_por_id(db, user_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        await usuario_repo.eliminar(db, user_id)
        return {"message": "Usuario eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))