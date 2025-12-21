from fastapi import APIRouter, HTTPException
from app.models.matricula_model import MatriculaBase, MatriculaOut
from app.services.matricula_service import MatriculaService
from app.models.DB import db

# Inicia la instancia del Router/Controlador
router = APIRouter()
matricula_service = MatriculaService(db)  # Instancia del servicio

@router.post("/", response_model=MatriculaOut)
def crear_matricula(matricula: MatriculaBase):
    """
    Crea una nueva matrícula en el sistema.
    """
    try:
        nuevo_matricula = matricula_service.create_matricula(matricula)
        return nuevo_matricula
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[MatriculaOut])
def obtener_matriculas():   
    """
    Obtiene todas las matrículas.
    """
    try:
        matriculas = matricula_service.get_all_matriculas()
        return matriculas
    except Exception as e:  # Para errores generales, como conexión a DB
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/{matricula_id}", response_model=MatriculaOut)
def obtener_matricula(matricula_id: str):
    """
    Obtiene la información de una matrícula por su ID.
    """
    try:
        matricula = matricula_service.get_matricula_by_id(matricula_id)
        return matricula
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{matricula_id}", response_model=MatriculaOut)
def actualizar_matricula(matricula_id: str, matricula: MatriculaBase):
    """
    Actualiza la información de una matrícula existente.
    """
    try:
        matricula_actualizada = matricula_service.update_matricula(matricula_id, matricula)
        return matricula_actualizada
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{matricula_id}")
def eliminar_matricula(matricula_id: str):
    """
    Elimina una matrícula del sistema.
    """
    try:
        exito = matricula_service.delete_matricula(matricula_id)
        return {"eliminado": exito}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))