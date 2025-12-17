from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.services.auth_service import AuthService

router = APIRouter(tags=["Autenticación"])
auth_service = AuthService()

@router.post("/login")
async def login(email: str, password: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    usuario = await auth_service.login(db, email, password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    return {
        "id": usuario["id"],
        "nombre": usuario["nombre"],
        "rol": usuario["rol"]
    }
