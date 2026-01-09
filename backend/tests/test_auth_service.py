import unittest
from mockito import when, mock, unstub, verify
import asyncio
from app.services.auth_service import AuthService

class TestAuthService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.auth_service = AuthService()
        self.mock_db = mock()

    async def asyncTearDown(self):
        unstub()

    def test_hash_password(self):
        # Setup manually for sync test if needed, or rely on setUp but access might be different
        service = AuthService()
        password = "secret_password"
        hashed = service.hash_password(password)
        self.assertNotEqual(password, hashed)
        self.assertTrue(service.verificar_password(password, hashed))

    async def test_login_success(self):
        email = "test@example.com"
        password = "password123"
        hashed_pw = self.auth_service.hash_password(password)
        
        user_data = {
            "email": email,
            "password": hashed_pw,
            "nombre": "Test User",
            "rol": "Estudiante",
            "id": "12345"
        }
        
        self.auth_service.repo = mock()
        
        # Create future inside the async test where loop is active
        future = asyncio.Future()
        future.set_result(user_data)
        when(self.auth_service.repo).obtener_por_email(self.mock_db, email).thenReturn(future)
        
        result = await self.auth_service.login(self.mock_db, email, password)
        
        self.assertEqual(result, user_data)
        verify(self.auth_service.repo).obtener_por_email(self.mock_db, email)

    async def test_login_failure_wrong_password(self):
        email = "test@example.com"
        password = "password123"
        hashed_pw = self.auth_service.hash_password("other_password")
        
        user_data = {
            "email": email,
            "password": hashed_pw,
            "nombre": "Test User",
            "rol": "Estudiante"
        }
        
        self.auth_service.repo = mock()
        future = asyncio.Future()
        future.set_result(user_data)
        when(self.auth_service.repo).obtener_por_email(self.mock_db, email).thenReturn(future)
        
        result = await self.auth_service.login(self.mock_db, email, password)
        
        self.assertIsNone(result)

    async def test_login_failure_user_not_found(self):
        email = "notfound@example.com"
        password = "password123"
        
        self.auth_service.repo = mock()
        future = asyncio.Future()
        future.set_result(None)
        when(self.auth_service.repo).obtener_por_email(self.mock_db, email).thenReturn(future)
        
        result = await self.auth_service.login(self.mock_db, email, password)
        
        self.assertIsNone(result)
