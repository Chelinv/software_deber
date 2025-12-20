from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.asignatura_controller import AsignaturaController
from app.controllers.grupo_controller import GrupoController

router = APIRouter(prefix="/asignaturas", tags=["Asignaturas"])

asignatura_controller = AsignaturaController()
grupo_controller = GrupoController()

@router.post("/")
def crear_asignatura(nombre: str, codigo: str,db: Session = Depends(get_db)):
    return asignatura_controller.crear(db, nombre, codigo)

@router.get("/")
def listar_asignaturas(db: Session = Depends(get_db)):
    return asignatura_controller.listar(db)

@router.post("/grupos")
def crear_grupo(nombre: str, aula: str,
                asignatura_id: int, docente_id: int,
                db: Session = Depends(get_db)):
    return grupo_controller.crear(
        db, nombre, aula, asignatura_id, docente_id
    )

@router.get("/grupos")
def listar_grupos(db: Session = Depends(get_db)):
    return grupo_controller.listar(db)
