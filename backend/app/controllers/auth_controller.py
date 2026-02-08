from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.services.auth_service import AuthService

from app.models.user_model import UserLogin

router = APIRouter(tags=["Autenticación"])
auth_service = AuthService()

@router.post("/login")
async def login(user_credentials: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db)):
    usuario = await auth_service.login(db, user_credentials.email, user_credentials.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "id": usuario["id"],
        "nombre": usuario["nombre"],
        "rol": usuario["rol"]
    }
