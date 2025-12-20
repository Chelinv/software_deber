from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.controllers.asignatura_controller import AsignaturaController
from app.controllers.grupo_controller import GrupoController
from app.models.asignatura import AsignaturaCreate, AsignaturaOut
from app.models.grupo import GrupoCreate, GrupoOut
from typing import List

router = APIRouter(tags=["Asignaturas"])

asignatura_controller = AsignaturaController()
grupo_controller = GrupoController()

@router.post("/", response_model=AsignaturaOut)
async def crear_asignatura(asignatura: AsignaturaCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await asignatura_controller.crear(db, asignatura.nombre, asignatura.codigo)

@router.get("/", response_model=List[AsignaturaOut])
async def listar_asignaturas(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await asignatura_controller.listar(db)

@router.post("/grupos", response_model=GrupoOut)
async def crear_grupo(grupo: GrupoCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await grupo_controller.crear(
        db, grupo.nombre, grupo.aula, grupo.asignatura_id, grupo.docente_id
    )

@router.get("/grupos", response_model=List[GrupoOut])
async def listar_grupos(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await grupo_controller.listar(db)
