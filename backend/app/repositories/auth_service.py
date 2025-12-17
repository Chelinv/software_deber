from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user_entity import Usuario
from app.repositories.user_repository import UsuarioRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    def __init__(self):
        self.repo = UsuarioRepository()

    def hash_password(self, password: str):
        return pwd_context.hash(password)

    def verificar_password(self, password: str, hashed: str):
        return pwd_context.verify(password, hashed)

    def registrar(self, db: Session, nombre, email, password, rol):
        usuario = Usuario(
            nombre=nombre,
            email=email,
            password=self.hash_password(password),
            rol=rol
        )
        return self.repo.crear(db, usuario)

    def login(self, db: Session, email, password):
        usuario = self.repo.obtener_por_email(db, email)
        if not usuario:
            return None
        if not self.verificar_password(password, usuario.password):
            return None
        return usuario
