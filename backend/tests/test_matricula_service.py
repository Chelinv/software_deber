import unittest
import asyncio
from mockito import when, mock, unstub, verify

from app.services.matricula_service import MatriculaService
from app.models.matricula_model import MatriculaCreate


class TestMatriculaService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = MatriculaService()
        self.mock_db = mock()
        self.service.repository = mock()

    async def asyncTearDown(self):
        unstub()

    async def test_create_matricula_validation_error(self):
        payload = MatriculaCreate(estudiante_id="", asignatura_id="a1", fecha_matricula="2023-01-01")
        with self.assertRaises(ValueError):
            await self.service.create_matricula(self.mock_db, payload)

    async def test_create_matricula_success(self):
        payload = MatriculaCreate(estudiante_id="e1", asignatura_id="a1", fecha_matricula="2023-01-01")
        created_dict = payload.model_dump()
        created_dict["id"] = "m1"

        future = asyncio.Future()
        future.set_result(created_dict)
        when(self.service.repository).create_matricula(self.mock_db, payload).thenReturn(future)

        result = await self.service.create_matricula(self.mock_db, payload)
        self.assertEqual(result.id, "m1")
        verify(self.service.repository).create_matricula(self.mock_db, payload)

    async def test_get_all_matriculas(self):
        m1 = {"id": "m1", "estudiante_id": "e1", "asignatura_id": "a1", "fecha_matricula": "2023-01-01"}
        m2 = {"id": "m2", "estudiante_id": "e2", "asignatura_id": "a1", "fecha_matricula": "2023-01-02"}

        future = asyncio.Future()
        future.set_result([m1, m2])
        when(self.service.repository).get_all_matriculas(self.mock_db).thenReturn(future)

        results = await self.service.get_all_matriculas(self.mock_db)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, "m1")

    async def test_get_matricula_by_id_not_found(self):
        future = asyncio.Future()
        future.set_result(None)
        when(self.service.repository).get_matricula_by_id(self.mock_db, "m404").thenReturn(future)

        with self.assertRaises(ValueError):
            await self.service.get_matricula_by_id(self.mock_db, "m404")

    async def test_update_matricula_success(self):
        payload = MatriculaCreate(estudiante_id="e1", asignatura_id="a1", fecha_matricula="2023-01-01")
        updated_dict = payload.model_dump()
        updated_dict["id"] = "m1"

        future = asyncio.Future()
        future.set_result(updated_dict)
        when(self.service.repository).update_matricula(self.mock_db, "m1", payload).thenReturn(future)

        result = await self.service.update_matricula(self.mock_db, "m1", payload)
        self.assertEqual(result.id, "m1")
        verify(self.service.repository).update_matricula(self.mock_db, "m1", payload)

    async def test_update_matricula_not_found(self):
        payload = MatriculaCreate(estudiante_id="e1", asignatura_id="a1", fecha_matricula="2023-01-01")

        future = asyncio.Future()
        future.set_result(None)
        when(self.service.repository).update_matricula(self.mock_db, "m404", payload).thenReturn(future)

        with self.assertRaises(ValueError):
            await self.service.update_matricula(self.mock_db, "m404", payload)

    async def test_delete_matricula(self):
        future = asyncio.Future()
        future.set_result(True)
        when(self.service.repository).delete_matricula(self.mock_db, "m1").thenReturn(future)

        result = await self.service.delete_matricula(self.mock_db, "m1")
        self.assertTrue(result)

