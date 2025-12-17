# app/api/endpoints/report_controller.py
from fastapi import APIRouter

from app.models.report_models import CertificadoAcademicoOut, HorarioClasesOut, RegistroAcademicoOut
from app.services.report_service import ReportService


router = APIRouter()
report_service = ReportService()


@router.get(
    "/certificados/{estudiante_id}",
    response_model=CertificadoAcademicoOut,
    summary="Generar Certificado Académico (RF 3.18)",
)
def generar_certificado(estudiante_id: int):
    """Servicio Web de Certificados Académicos (mínimo evaluable)."""
    return report_service.generar_certificado_academico(estudiante_id)


@router.get(
    "/record-academico/{estudiante_id}",
    response_model=RegistroAcademicoOut,
    summary="Generar Récord Académico",
)
def record_academico(estudiante_id: int):
    """Devuelve un resumen del récord académico del estudiante (simulado)."""
    return report_service.obtener_record_academico(estudiante_id)


@router.get(
    "/horario/{estudiante_id}",
    response_model=HorarioClasesOut,
    summary="Generar Horario de Clases",
)
def horario_clases(estudiante_id: int):
    """Devuelve el horario de clases del estudiante (simulado)."""
    return report_service.obtener_horario_clases(estudiante_id)
