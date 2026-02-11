from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from bson import ObjectId
from typing import List, Dict, Any

router = APIRouter()

@router.get("/estudiantes/{estudiante_id}/dashboard")
async def get_student_dashboard(
    estudiante_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Obtiene el dashboard completo de un estudiante:
    - Información del estudiante
    - Materias inscritas
    - Calificaciones de cada materia
    - Resumen académico
    """
    try:
        # Validar ObjectId
        if not ObjectId.is_valid(estudiante_id):
            raise HTTPException(status_code=400, detail="ID de estudiante inválido")
        
        # 1. Obtener información del estudiante
        estudiante = await db.usuarios.find_one({"_id": ObjectId(estudiante_id)})
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        # 2. Obtener matrícula del estudiante
        matricula = await db.matriculas.find_one({"estudiante_id": estudiante_id})
        
        materias_inscritas = []
        total_calificacion = 0
        materias_con_nota = 0
        materias_aprobadas = 0
        materias_reprobadas = 0
        
        if matricula and matricula.get("asignatura_ids"):
            # 3. Para cada asignatura inscrita, obtener información y calificación
            for asignatura_id in matricula["asignatura_ids"]:
                # Obtener información de la asignatura
                asignatura = await db.asignaturas.find_one({"_id": ObjectId(asignatura_id)})
                
                if asignatura:
                    # Buscar calificación del estudiante en esta asignatura
                    calificacion_doc = await db.calificaciones.find_one({
                        "estudiante_id": estudiante_id,
                        "asignatura_id": asignatura_id
                    })
                    
                    calificacion = None
                    estado = "En Curso"
                    
                    if calificacion_doc and calificacion_doc.get("calificacion") is not None:
                        calificacion = calificacion_doc["calificacion"]
                        total_calificacion += calificacion
                        materias_con_nota += 1
                        
                        # Determinar estado (nota mínima para aprobar: 7.0 en escala 0-10)
                        if calificacion >= 7.0:
                            estado = "Aprobado"
                            materias_aprobadas += 1
                        else:
                            estado = "Reprobado"
                            materias_reprobadas += 1
                    
                    materias_inscritas.append({
                        "asignatura_id": str(asignatura["_id"]),
                        "nombre": asignatura.get("nombre", "Sin nombre"),
                        "codigo": asignatura.get("codigo", "N/A"),
                        "calificacion": calificacion,
                        "estado": estado
                    })
        
        # 4. Calcular promedio general
        promedio_general = round(total_calificacion / materias_con_nota, 2) if materias_con_nota > 0 else None
        
        # 5. Construir respuesta
        dashboard_data = {
            "estudiante": {
                "id": str(estudiante["_id"]),
                "nombre": estudiante.get("nombre", "Sin nombre"),
                "email": estudiante.get("email", "Sin email")
            },
            "materias_inscritas": materias_inscritas,
            "resumen": {
                "total_materias": len(materias_inscritas),
                "materias_con_calificacion": materias_con_nota,
                "promedio_general": promedio_general,
                "materias_aprobadas": materias_aprobadas,
                "materias_reprobadas": materias_reprobadas,
                "materias_en_curso": len(materias_inscritas) - materias_con_nota
            }
        }
        
        return dashboard_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener dashboard: {str(e)}")
