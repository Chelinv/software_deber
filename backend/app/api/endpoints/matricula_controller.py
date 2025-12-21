from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.matricula_model import MatriculaCreate, MatriculaOut
from app.services.matricula_service import MatriculaService
from app.database import get_db

# Inicia la instancia del Router/Controlador
router = APIRouter()
matricula_service = MatriculaService()  # Instancia del servicio

@router.post("/", response_model=MatriculaOut)
async def crear_matricula(matricula: MatriculaCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Crea una nueva matrícula en el sistema.
    """
    try:
        nuevo_matricula = await matricula_service.create_matricula(db, matricula)
        return nuevo_matricula
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[MatriculaOut])
async def obtener_matriculas(db: AsyncIOMotorDatabase = Depends(get_db)):   
    """
    Obtiene todas las matrículas.
    """
    try:
        matriculas = await matricula_service.get_all_matriculas(db)
        return matriculas
    except Exception as e:  # Para errores generales, como conexión a DB
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/{matricula_id}", response_model=MatriculaOut)
async def obtener_matricula(matricula_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Obtiene la información de una matrícula por su ID.
    """
    try:
        matricula = await matricula_service.get_matricula_by_id(db, matricula_id)
        return matricula
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{matricula_id}", response_model=MatriculaOut)
async def actualizar_matricula(matricula_id: str, matricula: MatriculaCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Actualiza la información de una matrícula existente.
    """
    try:
        matricula_actualizada = await matricula_service.update_matricula(db, matricula_id, matricula)
        return matricula_actualizada
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{matricula_id}")
async def eliminar_matricula(matricula_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Elimina una matrícula del sistema.
    """
    try:
        exito = await matricula_service.delete_matricula(db, matricula_id)
        return {"eliminado": exito}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
