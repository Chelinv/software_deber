from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.calificaciones_model import CalificacionCreate, CalificacionOut
from app.services.calificaciones_service import CalificacionesService
from app.database import get_db

# Inicia la instancia del Router/Controlador
router = APIRouter()
calificaciones_service = CalificacionesService()  # Instancia del servicio

@router.post("/", response_model=CalificacionOut)
async def crear_calificacion(calificacion: CalificacionCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Crea una nueva calificación en el sistema.
    """
    try:
        nueva_calificacion = await calificaciones_service.create_calificacion(db, calificacion)
        return nueva_calificacion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 

@router.get("/", response_model=list[CalificacionOut])
async def obtener_calificaciones(db: AsyncIOMotorDatabase = Depends(get_db)):  
    """
    Obtiene todas las calificaciones.
    """
    try:
        calificaciones = await calificaciones_service.get_all_calificaciones(db)
        return calificaciones
    except Exception as e:  # Para errores generales, como conexión a DB
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/{calificacion_id}", response_model=CalificacionOut)
async def obtener_calificacion(calificacion_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Obtiene la información de una calificación por su ID.
    """
    try:
        calificacion = await calificaciones_service.get_calificacion_by_id(db, calificacion_id)
        return calificacion
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{calificacion_id}", response_model=CalificacionOut)
async def actualizar_calificacion(calificacion_id: str, calificacion: CalificacionCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Actualiza la información de una calificación existente.
    """
    try:
        calificacion_actualizada = await calificaciones_service.update_calificacion(db, calificacion_id, calificacion)
        return calificacion_actualizada
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{calificacion_id}")
async def eliminar_calificacion(calificacion_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Elimina una calificación del sistema.
    """
    try:
        exito = await calificaciones_service.delete_calificacion(db, calificacion_id)
        return {"exito": exito}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
