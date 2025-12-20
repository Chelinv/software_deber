from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import client
from app.controllers import user_controller, auth_controller
from app.api.endpoints import financial_controller, report_controller
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verificar conexión a MongoDB al iniciar
    try:
        await client.admin.command('ping')
        logger.info("¡Conexión exitosa a MongoDB Atlas!")
        print("\n" + "="*50)
        print("✅  CONEXIÓN A BASE DE DATOS EXITOSA")
        print("="*50 + "\n")
    except Exception as e:
        logger.error(f"Error al conectar a MongoDB: {e}")
        print("\n" + "="*50)
        print(f"❌  FALLO LA CONEXIÓN A BASE DE DATOS: {e}")
        print("="*50 + "\n")
    
    yield
    
    # Cerrar conexión al detener
    client.close()

# Inicializar la aplicación con lifespan
app = FastAPI(
    title="Sistema de Gestión de una Institución Educativa (SGIE) - Backend",
    description="Implementación del backend para la Tarea T02.03 utilizando FastAPI.",
    version="1.0.0",
    lifespan=lifespan
)

# Rutas de usuarios (CRUD)
app.include_router(
    user_controller.router,
    prefix="/api/v1/usuarios",
    tags=["Usuarios"]
)

# Rutas de autenticación (login)
app.include_router(
    auth_controller.router,
    prefix="/api/v1/auth",
    tags=["Autenticación"]
)
# Finanzas y Reportes (Xavier)
app.include_router(financial_controller.router, prefix="/api/v1/finanzas", tags=["Finanzas"])
app.include_router(report_controller.router, prefix="/api/v1/reportes", tags=["Reportes"])

# 🔹 NUEVO: Rutas de asignaturas y grupos
app.include_router(
    asignatura_api.router,
    prefix="/api/v1/asignaturas",
    tags=["Asignaturas"]
)

# Ruta raíz
@app.get("/")
def read_root():
    return {
        "message": "SGIE Backend funcionando correctamente. Ve a /docs para la documentación de la API."
    }
