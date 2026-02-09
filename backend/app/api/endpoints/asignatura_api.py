from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.controllers.asignatura_controller import AsignaturaController
from app.controllers.grupo_controller import GrupoController
from app.models.asignatura import AsignaturaCreate, AsignaturaInDB
from app.models.grupo import GrupoCreate, GrupoInDB

router = APIRouter()

asignatura_controller = AsignaturaController()
grupo_controller = GrupoController()

@router.post("/", response_model=AsignaturaInDB)
async def crear_asignatura(asignatura: AsignaturaCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await asignatura_controller.crear(db, asignatura.nombre, asignatura.codigo)

@router.get("/", response_model=list[AsignaturaInDB])
async def listar_asignaturas(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await asignatura_controller.listar(db)

@router.put("/{asignatura_id}", response_model=AsignaturaInDB)
async def actualizar_asignatura(
    asignatura_id: str,
    asignatura: AsignaturaCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    return await asignatura_controller.actualizar(db, asignatura_id, asignatura.nombre, asignatura.codigo)

@router.delete("/{asignatura_id}")
async def eliminar_asignatura(asignatura_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    await asignatura_controller.eliminar(db, asignatura_id)
    return {"message": "Asignatura eliminada exitosamente"}

@router.post("/grupos", response_model=GrupoInDB)
async def crear_grupo(grupo: GrupoCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await grupo_controller.crear(
        db, grupo.nombre, grupo.aula, grupo.asignatura_id, grupo.docente_id
    )

@router.get("/grupos", response_model=list[GrupoInDB])
async def listar_grupos(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await grupo_controller.listar(db)
