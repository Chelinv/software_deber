import unittest
from mockito import when, mock, unstub, verify, any as mockito_any
import asyncio
from app.services.calificaciones_service import CalificacionesService
from app.models.calificaciones_model import CalificacionCreate

class TestCalificacionesService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = CalificacionesService()
        self.mock_db = mock()
        self.service.repository = mock()

    async def asyncTearDown(self):
        unstub()

    async def test_create_calificacion(self):
        payload = CalificacionCreate(
            estudiante_id="est1",
            asignatura_id="asig1",
            calificacion=9.5,
            fecha_evaluacion="2023-01-01"
        )
        
        expected_dict = payload.model_dump()
        expected_dict["id"] = "cal1"
        
        future = asyncio.Future()
        future.set_result(expected_dict)
        when(self.service.repository).create_calificacion(self.mock_db, payload).thenReturn(future)
        
        result = await self.service.create_calificacion(self.mock_db, payload)
        
        self.assertEqual(result.id, "cal1")
        self.assertEqual(result.calificacion, 9.5)
        verify(self.service.repository).create_calificacion(self.mock_db, payload)

    async def test_get_all_calificaciones(self):
        cal1 = {"id": "c1", "estudiante_id": "e1", "asignatura_id": "a1", "calificacion": 8.0, "fecha_evaluacion": "2023"}
        cal2 = {"id": "c2", "estudiante_id": "e2", "asignatura_id": "a1", "calificacion": 9.0, "fecha_evaluacion": "2023"}
        
        future = asyncio.Future()
        future.set_result([cal1, cal2])
        when(self.service.repository).get_all_calificaciones(self.mock_db).thenReturn(future)
        
        results = await self.service.get_all_calificaciones(self.mock_db)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, "c1")

    async def test_get_calificacion_by_id_success(self):
        cal = {"id": "c1", "estudiante_id": "e1", "asignatura_id": "a1", "calificacion": 8.0, "fecha_evaluacion": "2023"}
        
        future = asyncio.Future()
        future.set_result(cal)
        when(self.service.repository).get_calificacion_by_id(self.mock_db, "c1").thenReturn(future)
        
        result = await self.service.get_calificacion_by_id(self.mock_db, "c1")
        
        self.assertEqual(result.id, "c1")

    async def test_get_calificacion_by_id_not_found(self):
        future = asyncio.Future()
        future.set_result(None)
        when(self.service.repository).get_calificacion_by_id(self.mock_db, "c99").thenReturn(future)
        
        with self.assertRaises(ValueError):
            await self.service.get_calificacion_by_id(self.mock_db, "c99")

    async def test_update_calificacion_success(self):
        payload = CalificacionCreate(
            estudiante_id="est1",
            asignatura_id="asig1",
            calificacion=9.8,
            fecha_evaluacion="2023-02-01"
        )
        updated_dict = payload.model_dump()
        updated_dict["id"] = "c1"

        future = asyncio.Future()
        future.set_result(updated_dict)
        when(self.service.repository).update_calificacion(self.mock_db, "c1", payload).thenReturn(future)

        result = await self.service.update_calificacion(self.mock_db, "c1", payload)
        self.assertEqual(result.id, "c1")
        self.assertEqual(result.calificacion, 9.8)
        verify(self.service.repository).update_calificacion(self.mock_db, "c1", payload)

    async def test_update_calificacion_not_found(self):
        payload = CalificacionCreate(
            estudiante_id="est1",
            asignatura_id="asig1",
            calificacion=9.8,
            fecha_evaluacion="2023-02-01"
        )

        future = asyncio.Future()
        future.set_result(None)
        when(self.service.repository).update_calificacion(self.mock_db, "c404", payload).thenReturn(future)

        with self.assertRaises(ValueError):
            await self.service.update_calificacion(self.mock_db, "c404", payload)

    async def test_delete_calificacion(self):
        future = asyncio.Future()
        future.set_result(True)
        when(self.service.repository).delete_calificacion(self.mock_db, "c1").thenReturn(future)
        
        result = await self.service.delete_calificacion(self.mock_db, "c1")
        self.assertTrue(result)
