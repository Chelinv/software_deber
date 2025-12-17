# app/models/report_models.py
from datetime import date
from pydantic import BaseModel, Field


class CertificadoAcademicoOut(BaseModel):
    """RF 3.18 - Servicio Web de Certificados Académicos (mínimo evaluable)."""

    estudiante_id: int = Field(..., examples=[101])
    estudiante_nombre: str = Field(..., examples=["Juan Pérez"])
    periodo: str = Field(..., examples=["2025-2"])
    fecha_emision: date = Field(..., examples=["2025-12-04"])
    codigo_verificacion: str = Field(..., examples=["CERT-2025-0001"])
    detalle: str = Field(..., examples=["Certifica que el estudiante se encuentra matriculado y activo."])


class RegistroAcademicoOut(BaseModel):
    estudiante_id: int
    estudiante_nombre: str
    promedio_general: float = Field(..., examples=[8.75])
    resumen: list[dict] = Field(
        ...,
        description="Lista simplificada de asignaturas y calificaciones.",
        examples=[[{"asignatura": "Matemáticas", "nota": 9.2}]],
    )


class HorarioClasesOut(BaseModel):
    estudiante_id: int
    estudiante_nombre: str
    horario: list[dict] = Field(
        ...,
        description="Lista simplificada de bloques de horario.",
        examples=[[{"dia": "Lunes", "hora": "08:00-10:00", "asignatura": "Lengua"}]],
    )
