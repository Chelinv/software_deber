from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
import io

from app.database import get_db
from app.models.report_models import CertificadoAcademicoOut, HorarioClasesOut, RegistroAcademicoOut
from app.services.report_service import ReportService


router = APIRouter()
report_service = ReportService()


@router.get(
    "/certificados/{estudiante_id}",
    summary="Generar Certificado Académico PDF (RF 3.18)",
)
async def generar_certificado(estudiante_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Genera y descarga un certificado académico en formato PDF."""
    pdf_bytes = await report_service.generar_certificado_pdf(db, estudiante_id)
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=certificado_{estudiante_id}.pdf"
        }
    )


@router.get(
    "/record-academico/{estudiante_id}",
    summary="Generar Récord Académico PDF",
)
async def record_academico(estudiante_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Genera y descarga el récord académico del estudiante en formato PDF."""
    pdf_bytes = await report_service.generar_record_academico_pdf(db, estudiante_id)
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=record_academico_{estudiante_id}.pdf"
        }
    )


@router.get(
    "/horario/{estudiante_id}",
    summary="Generar Horario de Clases PDF",
)
async def horario_clases(estudiante_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Genera y descarga el horario de clases del estudiante en formato PDF."""
    pdf_bytes = await report_service.generar_horario_pdf(db, estudiante_id)
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=horario_{estudiante_id}.pdf"
        }
    )
