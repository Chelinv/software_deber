from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import client
from app.controllers import user_controller, auth_controller
from app.api.endpoints import financial_controller, report_controller, matricula_controller, calificaciones_controller
import logging
import sys
from app.api.endpoints import asignatura_api
from app.models import asignatura, grupo

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verificar conexión a MongoDB al iniciar
    try:
        await client.admin.command('ping')
        print("\n" + "="*60)
        print("OK  CONEXION A BASE DE DATOS EXITOSA (MongoDB Atlas)")
        print("="*60 + "\n")
        logger.info("Conexion exitosa a MongoDB Atlas!")
    except Exception as e:
        print("\n" + "="*60)
        print("X  FALLO LA CONEXION A BASE DE DATOS")
        print(f"Error: {e}")
        print("="*60 + "\n")
        logger.error(f"Error al conectar a MongoDB: {e}")
    
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

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


app.include_router(matricula_controller.router, prefix="/api/v1/matriculas", tags=["Matrículas"])
app.include_router(calificaciones_controller.router, prefix="/api/v1/calificaciones", tags=["Calificaciones"])

# Ruta raíz
@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

#@app.get("/")
#def read_root():
#    return {
#        "message": [
#            "SGIE Backend funcionando correctamente.",
#            "Ve a /docs para la documentación de la API.",
#            "Para acceder a la lista de usuarios, ve a http://127.0.0.1:8000/api/v1/usuarios/",
#            "Para acceder a la lista de usuarios logeados, ve a http://127.0.0.1:8000/api/v1/auth",
#            "Para acceder a la lista de finanzas, ve a http://127.0.0.1:8000/api/v1/finanzas",
#            "Para acceder a la lista de reportes, ve a http://127.0.0.1:8000/api/v1/reportes",
#            "Para acceder a la lista de asignaturas, ve a http://127.0.0.1:8000/api/v1/asignaturas",
#            "Para acceder a la lista de matrículas, ve a http://127.0.0.1:8000/api/matriculas",
#            "Para acceder a la lista de calificaciones, ve a http://127.0.0.1:8000/api/calificaciones"
#        ]
#    }
    