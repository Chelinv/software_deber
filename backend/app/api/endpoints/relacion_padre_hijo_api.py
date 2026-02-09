from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.services.relacion_padre_hijo_service import RelacionPadreHijoService
from app.models.relacion_padre_hijo import RelacionPadreHijoCreate, RelacionPadreHijoOut
from typing import Optional

router = APIRouter()
service = RelacionPadreHijoService()

@router.post("/", response_model=RelacionPadreHijoOut)
async def crear_relacion(
    relacion: RelacionPadreHijoCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Crear o actualizar relación padre-hijo"""
    try:
        result = await service.crear_relacion(db, relacion.padre_id, relacion.estudiante_id)
        return RelacionPadreHijoOut(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/padre/{padre_id}/hijo")
async def obtener_hijo(
    padre_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener el estudiante asociado a un padre"""
    estudiante_id = await service.obtener_hijo_de_padre(db, padre_id)
    if not estudiante_id:
        raise HTTPException(status_code=404, detail="No se encontró estudiante asociado")
    
    # Obtener datos del estudiante
    estudiante = await db["usuarios"].find_one({"_id": estudiante_id})
    if estudiante:
        estudiante["id"] = str(estudiante["_id"])
        return estudiante
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")

@router.get("/estudiante/{estudiante_id}/padre")
async def obtener_padre(
    estudiante_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtener el padre asociado a un estudiante"""
    padre_id = await service.obtener_padre_de_estudiante(db, estudiante_id)
    if not padre_id:
        raise HTTPException(status_code=404, detail="No se encontró padre asociado")
    
    # Obtener datos del padre
    from bson import ObjectId
    padre = await db["usuarios"].find_one({"_id": ObjectId(padre_id)})
    if padre:
        padre["id"] = str(padre["_id"])
        return padre
    raise HTTPException(status_code=404, detail="Padre no encontrado")
