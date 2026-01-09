import unittest
import asyncio
from mockito import when, mock, unstub, verify, any as mockito_any

from app.services.asignatura_service import AsignaturaService


class TestAsignaturaService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = AsignaturaService()
        self.mock_db = mock()
        self.service.repo = mock()

    async def asyncTearDown(self):
        unstub()

    async def test_crear(self):
        future = asyncio.Future()
        future.set_result({"id": "a1", "nombre": "Matemáticas", "codigo": "MAT-01"})
        when(self.service.repo).crear(self.mock_db, mockito_any()).thenReturn(future)

        result = await self.service.crear(self.mock_db, "Matemáticas", "MAT-01")
        self.assertEqual(result["codigo"], "MAT-01")
        verify(self.service.repo).crear(self.mock_db, mockito_any())

    async def test_listar(self):
        future = asyncio.Future()
        future.set_result([{"id": "a1", "nombre": "Matemáticas", "codigo": "MAT-01"}])
        when(self.service.repo).listar(self.mock_db).thenReturn(future)

        result = await self.service.listar(self.mock_db)
        self.assertEqual(len(result), 1)
        verify(self.service.repo).listar(self.mock_db)
