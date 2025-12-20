# app/api/endpoints/user_controller.py
from fastapi import APIRouter
from app.models.user_model import UserOut # Importación temporal
from app.services.user_service import UserService # Importación temporal

# Inicia la instancia del Router/Controlador
router = APIRouter()
user_service = UserService() # Instancia del servicio

# Ruta para la creación de un usuario (ejemplo inicial para el equipo)
# Stefany usará esto para probar su lógica
@router.post("/", response_model=UserOut)
def crear_usuario(user: UserOut): # Se usa UserOut temporalmente
    """
    Registra un nuevo usuario en el sistema.
    """
    # Llama a la lógica de negocio del servicio
    nuevo_usuario = user_service.create_user(user) 
    return nuevo_usuario

@router.get("/{user_id}", response_model=UserOut)
def obtener_usuario(user_id: int):
    """
    Obtiene la información de un usuario por su ID.
    """
    # Llama a la lógica de negocio del servicio
    usuario = user_service.get_user(user_id) 
    return usuario