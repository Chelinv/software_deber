from passlib.context import CryptContext
from app.repositories.user_repository import UsuarioRepository
from motor.motor_asyncio import AsyncIOMotorDatabase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    def __init__(self):
        self.repo = UsuarioRepository()

    def hash_password(self, password: str):
        return pwd_context.hash(password)

    def verificar_password(self, password: str, hashed: str):
        return pwd_context.verify(password, hashed)

    async def registrar(self, db: AsyncIOMotorDatabase, nombre, email, password, rol):
        usuario = {
            "nombre": nombre,
            "email": email,
            "password": self.hash_password(password),
            "rol": rol
        }
        return await self.repo.crear(db, usuario)

    async def login(self, db: AsyncIOMotorDatabase, email, password):
        usuario = await self.repo.obtener_por_email(db, email)
        if not usuario:
            return None
        if not self.verificar_password(password, usuario["password"]):
            return None
        return usuario
