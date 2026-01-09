# app/services/user_service.py
from app.models.user_model import UserOut
# En este punto, el servicio NO llama al repositorio, solo devuelve datos de prueba.

class UserService:
    def create_user(self, user: UserOut) -> UserOut:
        """Lógica de negocio: Valida y registra un nuevo usuario."""
        # TODO: Lógica de Stefany. Por ahora, solo devuelve el objeto de entrada con un ID
        user.id = "1" # ID de prueba
        return user

    def get_user(self, user_id: int) -> UserOut:
        """Lógica de negocio: Busca un usuario por ID."""
        # TODO: Lógica de Stefany. Por ahora, datos de prueba fijos
        if user_id == 1:
            return UserOut(id="1", nombre="Celine", email="celine@sge.com", rol="Administrador")
        else:
            return UserOut(id=str(user_id), nombre="Usuario de Prueba", email="prueba@sge.com", rol="Estudiante")