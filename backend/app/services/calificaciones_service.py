from typing import List
from app.models.calificaciones_model import CalificacionBase, CalificacionOut  
from app.repositories.calificaciones_repository import CalificacionesRepository

class CalificacionesService:
    def __init__(self, db_session):
        self.repository = CalificacionesRepository(db_session)

    def create_calificacion(self, calificacion: CalificacionBase) -> CalificacionOut:
        """Lógica de negocio: Valida y crea una calificación."""
        if calificacion.asignatura_id <= 0 or not (0 <= calificacion.calificacion <= 100):
            raise ValueError("asignatura_id debe ser positivo y calificación entre 0 y 100")
        created_calificacion = self.repository.create_calificacion(calificacion)
        return CalificacionOut.model_validate(created_calificacion)  

    def get_all_calificaciones(self) -> List[CalificacionOut]:
        """Obtiene todas las calificaciones."""
        calificaciones = self.repository.get_all_calificaciones()
        return [CalificacionOut.model_validate(calificacion) for calificacion in calificaciones]

    def get_calificacion_by_id(self, calificacion_id: str) -> CalificacionOut:  
        """Obtiene una calificación por ID."""
        calificacion = self.repository.get_calificacion_by_id(calificacion_id)
        if not calificacion:
            raise ValueError(f"Calificación con ID {calificacion_id} no encontrada")
        return CalificacionOut.model_validate(calificacion)

    def update_calificacion(self, calificacion_id: str, updated_calificacion: CalificacionBase) -> CalificacionOut:  
        """Actualiza una calificación."""
        updated = self.repository.update_calificacion(calificacion_id, updated_calificacion)
        if not updated:
            raise ValueError(f"Calificación con ID {calificacion_id} no encontrada")
        return CalificacionOut.model_validate(updated)

    def delete_calificacion(self, calificacion_id: str) -> bool:  
        """Elimina una calificación."""
        return self.repository.delete_calificacion(calificacion_id)