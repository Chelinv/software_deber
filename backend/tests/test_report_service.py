import unittest
import asyncio
from mockito import when, mock, unstub, verify

from app.services.report_service import ReportService


class TestReportService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = ReportService()
        self.mock_db = mock()
        self.service.user_repo = mock()

    async def asyncTearDown(self):
        unstub()

    async def test_get_student_name_from_db(self):
        future = asyncio.Future()
        future.set_result({"nombre": "Ana"})
        when(self.service.user_repo).obtener_por_id(self.mock_db, "u1").thenReturn(future)

        name = await self.service._get_student_name(self.mock_db, "u1")
        self.assertEqual(name, "Ana")
        verify(self.service.user_repo).obtener_por_id(self.mock_db, "u1")

    async def test_get_student_name_fallback(self):
        future = asyncio.Future()
        future.set_result(None)
        when(self.service.user_repo).obtener_por_id(self.mock_db, "u2").thenReturn(future)

        name = await self.service._get_student_name(self.mock_db, "u2")
        self.assertEqual(name, "Estudiante u2")

    async def test_generar_certificado_academico(self):
        future = asyncio.Future()
        future.set_result({"nombre": "Luis"})
        when(self.service.user_repo).obtener_por_id(self.mock_db, "abcd1234").thenReturn(future)

        result = await self.service.generar_certificado_academico(self.mock_db, "abcd1234")
        self.assertEqual(result.estudiante_id, "abcd1234")
        self.assertEqual(result.estudiante_nombre, "Luis")
        self.assertEqual(result.periodo, "2025-2")
        self.assertIn("CERT-2025-", result.codigo_verificacion)

    async def test_obtener_record_academico(self):
        future = asyncio.Future()
        future.set_result(None)
        when(self.service.user_repo).obtener_por_id(self.mock_db, "x").thenReturn(future)

        result = await self.service.obtener_record_academico(self.mock_db, "x")
        self.assertEqual(result.estudiante_id, "x")
        self.assertEqual(result.estudiante_nombre, "Estudiante x")
        self.assertTrue(len(result.resumen) >= 1)

    async def test_obtener_horario_clases(self):
        future = asyncio.Future()
        future.set_result(None)
        when(self.service.user_repo).obtener_por_id(self.mock_db, "y").thenReturn(future)

        result = await self.service.obtener_horario_clases(self.mock_db, "y")
        self.assertEqual(result.estudiante_id, "y")
        self.assertEqual(result.estudiante_nombre, "Estudiante y")
        self.assertTrue(len(result.horario) >= 1)

