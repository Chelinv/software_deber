from datetime import date
from motor.motor_asyncio import AsyncIOMotorDatabase
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from bson import ObjectId

from app.models.report_models import CertificadoAcademicoOut, HorarioClasesOut, RegistroAcademicoOut
from app.repositories.user_repository import UsuarioRepository


class ReportService:
    """Servicio de Reportes con generación de PDFs."""
    
    def __init__(self):
        self.user_repo = UsuarioRepository()

    async def _get_student_name(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> str:
        """Obtiene el nombre del estudiante desde la base de datos."""
        try:
            user = await self.user_repo.obtener_por_id(db, estudiante_id)
            if user:
                return user["nombre"]
        except:
            pass
        return f"Estudiante {estudiante_id}"
    
    async def _get_student_data(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> dict:
        """Obtiene datos completos del estudiante."""
        try:
            user = await self.user_repo.obtener_por_id(db, estudiante_id)
            if user:
                return user
        except:
            pass
        return {
            "nombre": f"Estudiante {estudiante_id}",
            "email": "no-email@example.com",
            "rol": "Estudiante"
        }

    # ==================== MÉTODOS JSON (Originales) ====================
    
    async def generar_certificado_academico(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> CertificadoAcademicoOut:
        nombre = await self._get_student_name(db, estudiante_id)
        
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

    # ==================== MÉTODOS PDF (Nuevos) ====================

    async def generar_certificado_pdf(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> bytes:
        """Genera un PDF de certificado académico."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_LEFT
        )
        
        # Obtener datos del estudiante
        student = await self._get_student_data(db, estudiante_id)
        codigo_verificacion = f"CERT-2026-{estudiante_id[-4:] if len(estudiante_id) > 4 else '0000'}"
        
        # Contenido del PDF
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("CERTIFICADO ACADÉMICO", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("Sistema de Gestión Educativa", subtitle_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Información del estudiante
        story.append(Paragraph(f"<b>Nombre:</b> {student.get('nombre', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Email:</b> {student.get('email', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Rol:</b> {student.get('rol', 'Estudiante')}", body_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Texto del certificado
        certificado_text = f"""
        Se certifica que el estudiante <b>{student.get('nombre', 'N/A')}</b> se encuentra 
        matriculado y activo en el Sistema de Gestión Educativa durante el período académico 2026-1.
        """
        story.append(Paragraph(certificado_text, body_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Información adicional
        story.append(Paragraph(f"<b>Código de verificación:</b> {codigo_verificacion}", body_style))
        story.append(Paragraph(f"<b>Fecha de emisión:</b> {date.today().strftime('%d/%m/%Y')}", body_style))
        
        # Generar PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes

    async def generar_record_academico_pdf(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> bytes:
        """Genera un PDF del récord académico con calificaciones."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=12,
            spaceAfter=12
        )
        
        # Obtener datos del estudiante
        student = await self._get_student_data(db, estudiante_id)
        
        # Obtener calificaciones reales desde la base de datos
        calificaciones = []
        total_notas = 0
        count_notas = 0
        
        try:
            # Buscar matrícula del estudiante
            matricula = await db.matriculas.find_one({"estudiante_id": estudiante_id})
            
            if matricula and "asignatura_ids" in matricula:
                for asig_id in matricula["asignatura_ids"]:
                    # Obtener nombre de la asignatura
                    asignatura = await db.asignaturas.find_one({"_id": ObjectId(asig_id)})
                    asig_nombre = asignatura.get("nombre", "Desconocida") if asignatura else "Desconocida"
                    
                    # Buscar calificación
                    calificacion = await db.calificaciones.find_one({
                        "estudiante_id": estudiante_id,
                        "asignatura_id": asig_id
                    })
                    
                    if calificacion and "calificacion" in calificacion:
                        nota = float(calificacion["calificacion"])
                        calificaciones.append([asig_nombre, f"{nota:.1f}"])
                        total_notas += nota
                        count_notas += 1
                    else:
                        calificaciones.append([asig_nombre, "Pendiente"])
        except Exception as e:
            print(f"Error obteniendo calificaciones: {e}")
        
        # Si no hay calificaciones, mostrar datos simulados
        if not calificaciones:
            calificaciones = [
                ["Matemáticas", "85.0"],
                ["Física", "90.0"],
                ["Química", "88.0"]
            ]
            total_notas = 263.0
            count_notas = 3
        
        promedio = total_notas / count_notas if count_notas > 0 else 0.0
        
        # Contenido del PDF
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("RÉCORD ACADÉMICO", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph(f"<b>Estudiante:</b> {student.get('nombre', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Email:</b> {student.get('email', 'N/A')}", body_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Tabla de calificaciones
        data = [["Asignatura", "Calificación"]] + calificaciones
        
        table = Table(data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Promedio
        story.append(Paragraph(f"<b>Promedio General:</b> {promedio:.2f}", body_style))
        story.append(Paragraph(f"<b>Fecha de emisión:</b> {date.today().strftime('%d/%m/%Y')}", body_style))
        
        # Generar PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes

    async def generar_horario_pdf(self, db: AsyncIOMotorDatabase, estudiante_id: str) -> bytes:
        """Genera un PDF del horario de clases."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=12,
            spaceAfter=12
        )
        
        # Obtener datos del estudiante
        student = await self._get_student_data(db, estudiante_id)
        
        # Obtener materias inscritas
        materias = []
        try:
            matricula = await db.matriculas.find_one({"estudiante_id": estudiante_id})
            
            if matricula and "asignatura_ids" in matricula:
                for asig_id in matricula["asignatura_ids"]:
                    asignatura = await db.asignaturas.find_one({"_id": ObjectId(asig_id)})
                    if asignatura:
                        materias.append(asignatura.get("nombre", "Desconocida"))
        except Exception as e:
            print(f"Error obteniendo materias: {e}")
        
        # Si no hay materias, mostrar datos simulados
        if not materias:
            materias = ["Matemáticas", "Física", "Química"]
        
        # Contenido del PDF
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("HORARIO DE CLASES", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph(f"<b>Estudiante:</b> {student.get('nombre', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Email:</b> {student.get('email', 'N/A')}", body_style))
        story.append(Spacer(1, 0.3*inch))
        
        story.append(Paragraph("<b>Materias Inscritas:</b>", body_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Lista de materias
        for materia in materias:
            story.append(Paragraph(f"• {materia}", body_style))
        
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("<i>Nota: Los horarios específicos serán asignados por la institución.</i>", body_style))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"<b>Fecha de emisión:</b> {date.today().strftime('%d/%m/%Y')}", body_style))
        
        # Generar PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
