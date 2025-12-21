from typing import List
from app.models.matricula_model import MatriculaBase, MatriculaOut  # Asumiendo Matricula para entrada y MatriculaOut para salida
from app.repositories.matricula_repository import MatriculaRepository

class MatriculaService:
    def __init__(self, db_session):
        self.repository = MatriculaRepository(db_session)

    def create_matricula(self, matricula: MatriculaBase) -> MatriculaOut:
        """Lógica de negocio: Valida y crea una matrícula."""
        # Validación básica (ejemplo)
        if matricula.estudiante_id <= 0 or matricula.asignatura_id <= 0:
            raise ValueError("estudiante_id y asignatura_id deben ser positivos")
        created_matricula = self.repository.create_matricula(matricula)
        return MatriculaOut.model_validate(created_matricula)  # Asumiendo Pydantic para conversión

    def get_all_matriculas(self) -> List[MatriculaOut]:
        """Obtiene todas las matrículas."""
        matriculas = self.repository.get_all_matriculas()
        return [MatriculaOut.model_validate(matricula) for matricula in matriculas]

    def get_matricula_by_id(self, matricula_id: str) -> MatriculaOut:  # Ya es str
        """Obtiene una matrícula por ID."""
        matricula = self.repository.get_matricula_by_id(matricula_id)
        if not matricula:
            raise ValueError(f"Matrícula con ID {matricula_id} no encontrada")
        return MatriculaOut.model_validate(matricula)

    def update_matricula(self, matricula_id: str, updated_matricula: MatriculaBase) -> MatriculaOut:  # Ya es str
        """Actualiza una matrícula."""
        updated = self.repository.update_matricula(matricula_id, updated_matricula)
        if not updated:
            raise ValueError(f"Matrícula con ID {matricula_id} no encontrada")
        return MatriculaOut.model_validate(updated)

    def delete_matricula(self, matricula_id: str) -> bool:  # Ya es str
        """Elimina una matrícula."""
        return self.repository.delete_matricula(matricula_id)