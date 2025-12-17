# app/services/report_service.py
from datetime import date

from app.models.report_models import CertificadoAcademicoOut, HorarioClasesOut, RegistroAcademicoOut


class ReportService:
    """Servicio de Reportes (mínimo evaluable).

    Nota: Retorna datos simulados para demostrar el API y la documentación en Swagger.
    """

    def generar_certificado_academico(self, estudiante_id: int) -> CertificadoAcademicoOut:
        # Datos simulados (en un siguiente avance se conectaría a Matrículas/Calificaciones)
        return CertificadoAcademicoOut(
            estudiante_id=estudiante_id,
            estudiante_nombre=f"Estudiante {estudiante_id}",
            periodo="2025-2",
            fecha_emision=date.today(),
            codigo_verificacion=f"CERT-2025-{estudiante_id:04d}",
            detalle="Certifica que el estudiante se encuentra matriculado y activo.",
        )

    def obtener_record_academico(self, estudiante_id: int) -> RegistroAcademicoOut:
        return RegistroAcademicoOut(
            estudiante_id=estudiante_id,
            estudiante_nombre=f"Estudiante {estudiante_id}",
            promedio_general=8.75,
            resumen=[
                {"asignatura": "Matemáticas", "nota": 9.2},
                {"asignatura": "Lengua", "nota": 8.4},
            ],
        )

    def obtener_horario_clases(self, estudiante_id: int) -> HorarioClasesOut:
        return HorarioClasesOut(
            estudiante_id=estudiante_id,
            estudiante_nombre=f"Estudiante {estudiante_id}",
            horario=[
                {"dia": "Lunes", "hora": "08:00-10:00", "asignatura": "Matemáticas"},
                {"dia": "Miércoles", "hora": "10:00-12:00", "asignatura": "Lengua"},
            ],
        )
