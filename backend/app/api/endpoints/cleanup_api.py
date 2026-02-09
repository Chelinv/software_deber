from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/cleanup-orphaned-subjects")
async def cleanup_orphaned_subjects(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Limpia referencias a asignaturas que ya no existen en las matrículas.
    """
    # Obtener todas las asignaturas válidas
    asignaturas_cursor = db["asignaturas"].find({})
    valid_asignatura_ids = set()
    async for asignatura in asignaturas_cursor:
        valid_asignatura_ids.add(str(asignatura["_id"]))
    
    # Obtener todas las matrículas
    matriculas_cursor = db["matriculas"].find({})
    cleaned_count = 0
    removed_ids = []
    
    async for matricula in matriculas_cursor:
        original_ids = matricula.get("asignatura_ids", [])
        
        # Filtrar solo IDs válidos
        valid_ids = [aid for aid in original_ids if aid in valid_asignatura_ids]
        
        # Si hay diferencia, actualizar
        if len(valid_ids) != len(original_ids):
            removed = [aid for aid in original_ids if aid not in valid_asignatura_ids]
            removed_ids.extend(removed)
            
            if len(valid_ids) > 0:
                # Actualizar con IDs válidos
                await db["matriculas"].update_one(
                    {"_id": matricula["_id"]},
                    {"$set": {"asignatura_ids": valid_ids}}
                )
                cleaned_count += 1
            else:
                # Si no quedan asignaturas válidas, eliminar la matrícula completa
                await db["matriculas"].delete_one({"_id": matricula["_id"]})
                cleaned_count += 1
    
    return {
        "message": "Limpieza completada",
        "matriculas_cleaned": cleaned_count,
        "invalid_subject_ids_removed": list(set(removed_ids)),
        "valid_subject_ids": list(valid_asignatura_ids)
    }
