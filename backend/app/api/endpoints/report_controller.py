from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_db
from app.models.report_models import CertificadoAcademicoOut, HorarioClasesOut, RegistroAcademicoOut
from app.services.report_service import ReportService


router = APIRouter()
report_service = ReportService()


@router.get(
    "/certificados/{estudiante_id}",
    response_model=CertificadoAcademicoOut,
    summary="Generar Certificado Académico (RF 3.18)",
)
async def generar_certificado(estudiante_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Servicio Web de Certificados Académicos (mínimo evaluable)."""
    return await report_service.generar_certificado_academico(db, estudiante_id)


@router.get(
    "/record-academico/{estudiante_id}",
    response_model=RegistroAcademicoOut,
    summary="Generar Récord Académico",
)
async def record_academico(estudiante_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Devuelve un resumen del récord académico del estudiante (simulado)."""
    return await report_service.obtener_record_academico(db, estudiante_id)


@router.get(
    "/horario/{estudiante_id}",
    response_model=HorarioClasesOut,
    summary="Generar Horario de Clases",
)
async def horario_clases(estudiante_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Devuelve el horario de clases del estudiante (simulado)."""
    return await report_service.obtener_horario_clases(db, estudiante_id)
