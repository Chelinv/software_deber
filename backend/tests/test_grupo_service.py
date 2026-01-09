import unittest
import asyncio
from mockito import when, mock, unstub, verify, any as mockito_any

from app.services.grupo_service import GrupoService


class TestGrupoService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = GrupoService()
        self.mock_db = mock()
        self.service.repo = mock()

    async def asyncTearDown(self):
        unstub()

    async def test_crear(self):
        future = asyncio.Future()
        future.set_result({"id": "g1", "nombre": "Grupo A", "aula": "101", "asignatura_id": "a1", "docente_id": "d1"})
        when(self.service.repo).crear(self.mock_db, mockito_any()).thenReturn(future)

        result = await self.service.crear(self.mock_db, "Grupo A", "101", "a1", "d1")
        self.assertEqual(result["id"], "g1")
        verify(self.service.repo).crear(self.mock_db, mockito_any())

    async def test_listar(self):
        future = asyncio.Future()
        future.set_result([{"id": "g1", "nombre": "Grupo A", "aula": "101", "asignatura_id": "a1", "docente_id": "d1"}])
        when(self.service.repo).listar(self.mock_db).thenReturn(future)

        result = await self.service.listar(self.mock_db)
        self.assertEqual(len(result), 1)
        verify(self.service.repo).listar(self.mock_db)
