import unittest
from app.services.user_service import UserService
from app.models.user_model import UserOut
from app.models.user_entity import RolEnum

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.service = UserService()

    def test_create_user(self):
        user_in = UserOut(id="0", nombre="Test", email="test@test.com", rol=RolEnum.estudiante)
        result = self.service.create_user(user_in)
        self.assertEqual(result.id, "1") # UserService hardcodes id="1"
        self.assertEqual(result.nombre, "Test")

    def test_get_user(self):
        # Case id=1
        user1 = self.service.get_user(1)
        self.assertEqual(user1.id, "1")
        self.assertEqual(user1.nombre, "Celine")

        # Case other id
        user2 = self.service.get_user(99)
        self.assertEqual(user2.id, "99")
        self.assertEqual(user2.nombre, "Usuario de Prueba")

    def test_rol_enum(self):
        self.assertEqual(RolEnum.administrador, "Administrador")
        self.assertEqual(RolEnum.docente, "Docente")
