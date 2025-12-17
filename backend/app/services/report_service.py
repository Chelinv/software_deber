from datetime import date
from motor.motor_asyncio import AsyncIOMotorDatabase
# from fastapi import HTTPException  # Unused


from app.models.report_models import CertificadoAcademicoOut, HorarioClasesOut, RegistroAcademicoOut
from app.repositories.user_repository import UsuarioRepository


class ReportService:
    """Servicio de Reportes (mínimo evaluable).
    
    Nota: Retorna datos simulados para demostrar el API y la documentación en Swagger.
    """
    
    def __init__(self):
        self.user_repo = UsuarioRepository()

    async def _get_student_name(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> str:
        # Intenta obtener el nombre real si existe en la base de datos
        user = await self.user_repo.obtener_por_id(db, estudiante_id)
        if user:
            return user["nombre"]
        return f"Estudiante {estudiante_id}"

    async def generar_certificado_academico(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> CertificadoAcademicoOut:
        nombre = await self._get_student_name(db, estudiante_id)
        
        # Datos simulados (en un siguiente avance se conectaría a Matrículas/Calificaciones)
        return CertificadoAcademicoOut(
            estudiante_id=estudiante_id,
            estudiante_nombre=nombre,
            periodo="2025-2",
            fecha_emision=date.today(),
            codigo_verificacion=f"CERT-2025-{estudiante_id[-4:] if len(estudiante_id) > 4 else '0000'}",
            detalle="Certifica que el estudiante se encuentra matriculado y activo.",
        )

    async def obtener_record_academico(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> RegistroAcademicoOut:
        nombre = await self._get_student_name(db, estudiante_id)
        
        return RegistroAcademicoOut(
            estudiante_id=estudiante_id,
            estudiante_nombre=nombre,
            promedio_general=8.75,
            resumen=[
                {"asignatura": "Matemáticas", "nota": 9.2},
                {"asignatura": "Lengua", "nota": 8.4},
            ],
        )

    async def obtener_horario_clases(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> HorarioClasesOut:
        nombre = await self._get_student_name(db, estudiante_id)
        
        return HorarioClasesOut(
            estudiante_id=estudiante_id,
            estudiante_nombre=nombre,
            horario=[
                {"dia": "Lunes", "hora": "08:00-10:00", "asignatura": "Matemáticas"},
                {"dia": "Miércoles", "hora": "10:00-12:00", "asignatura": "Lengua"},
            ],
        )
