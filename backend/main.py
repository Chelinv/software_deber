# main.py
from fastapi import FastAPI
from app.api.endpoints import user_controller

# Inicializar la aplicación
app = FastAPI(
    title="Sistema de Gestión de una Institución Educativa (SGIE) - Backend",
    description="Implementación del backend para la Tarea T02.03 utilizando FastAPI.",
    version="1.0.0",
)

# Incluir el primer controlador/router
app.include_router(user_controller.router, prefix="/api/v1/usuarios", tags=["Usuarios"])

@app.get("/")
def read_root():
    return {"message": "SGIE Backend funcionando correctamente. Ve a /docs para la documentación de la API."}

# Nota: El servidor Uvicorn se iniciará con un comando aparte (ver paso 3)