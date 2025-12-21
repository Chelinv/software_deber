from fastapi import APIRouter, HTTPException
from app.models.calificaciones_model import CalificacionBase, CalificacionOut
from app.services.calificaciones_service import CalificacionesService
from app.models.DB import db

# Inicia la instancia del Router/Controlador
router = APIRouter()
calificaciones_service = CalificacionesService(db)  # Instancia del servicio
@router.post("/", response_model=CalificacionOut)
def crear_calificacion(calificacion: CalificacionBase):
    """
    Crea una nueva calificación en el sistema.
    """
    try:
        nueva_calificacion = calificaciones_service.create_calificacion(calificacion)
        return nueva_calificacion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 
@router.get("/", response_model=list[CalificacionOut])
def obtener_calificaciones():  
    """
    Obtiene todas las calificaciones.
    """
    try:
        calificaciones = calificaciones_service.get_all_calificaciones()
        return calificaciones
    except Exception as e:  # Para errores generales, como conexión a DB
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
@router.get("/{calificacion_id}", response_model=CalificacionOut)
def obtener_calificacion(calificacion_id: str):
    """
    Obtiene la información de una calificación por su ID.
    """
    try:
        calificacion = calificaciones_service.get_calificacion_by_id(calificacion_id)
        return calificacion
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
@router.put("/{calificacion_id}", response_model=CalificacionOut)
def actualizar_calificacion(calificacion_id: str, calificacion: CalificacionBase):
    """
    Actualiza la información de una calificación existente.
    """
    try:
        calificacion_actualizada = calificaciones_service.update_calificacion(calificacion_id, calificacion)
        return calificacion_actualizada
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
@router.delete("/{calificacion_id}")
def eliminar_calificacion(calificacion_id: str):
    """
    Elimina una calificación del sistema.
    """
    try:
        exito = calificaciones_service.delete_calificacion(calificacion_id)
        return {"exito": exito}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
