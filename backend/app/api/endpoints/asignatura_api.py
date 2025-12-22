from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.controllers.asignatura_controller import AsignaturaController
from app.controllers.grupo_controller import GrupoController

router = APIRouter()

asignatura_controller = AsignaturaController()
grupo_controller = GrupoController()

@router.post("/")
async def crear_asignatura(nombre: str, codigo: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await asignatura_controller.crear(db, nombre, codigo)

@router.get("/")
async def listar_asignaturas(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await asignatura_controller.listar(db)

@router.post("/grupos")
async def crear_grupo(nombre: str, aula: str,
                asignatura_id: str, docente_id: str,
                db: AsyncIOMotorDatabase = Depends(get_db)):
    return await grupo_controller.crear(
        db, nombre, aula, asignatura_id, docente_id
    )

@router.get("/grupos")
async def listar_grupos(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await grupo_controller.listar(db)
