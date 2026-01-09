import unittest
from mockito import when, mock, unstub, verify, any as mockito_any
import asyncio
from fastapi import HTTPException
from app.services.financial_service import FinancialService
from app.models.transaction_model import TransactionIn

class TestFinancialService(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.service = FinancialService()
        self.mock_db = mock()
        # Mock repositories injected in __init__
        self.service.accounts = mock()
        self.service.transactions = mock()
        self.service.vouchers = mock()

    async def asyncTearDown(self):
        unstub()

    async def test_create_transaction_debito(self):
        payload = TransactionIn(
            cuenta_id="acc1",
            tipo="DEBITO",
            monto=100.0,
            descripcion="Deposito"
        )
        
        # Mock account
        account_data = {"id": "acc1", "saldo": 50.0, "nombre": "Banco", "codigo": "111"}
        future_acc = asyncio.Future()
        future_acc.set_result(account_data)
        when(self.service.accounts).get(self.mock_db, "acc1").thenReturn(future_acc)
        
        # Mock update saldo
        future_update = asyncio.Future()
        future_update.set_result(None)
        when(self.service.accounts).update_saldo(self.mock_db, "acc1", 150.0).thenReturn(future_update)
        
        # Mock create transaction
        tx_data = payload.model_dump()
        tx_data["id"] = "tx1"
        tx_data["fecha"] = "2023-01-01" # Fake date
        future_tx = asyncio.Future()
        future_tx.set_result(tx_data)
        when(self.service.transactions).create(self.mock_db, mockito_any()).thenReturn(future_tx)
        
        # Mock create voucher
        voucher_data = {"id": "v1"}
        future_v = asyncio.Future()
        future_v.set_result(voucher_data)
        when(self.service.vouchers).create(self.mock_db, mockito_any()).thenReturn(future_v)
        
        # Mock update transaction with voucher
        future_up_tx = asyncio.Future()
        future_up_tx.set_result(None)
        when(self.service.transactions).update(self.mock_db, "tx1", mockito_any()).thenReturn(future_up_tx)
        
        result = await self.service.create_transaction(self.mock_db, payload)
        
        self.assertEqual(result.monto, 100.0)
        self.assertEqual(result.comprobante_id, "v1")
        verify(self.service.accounts).update_saldo(self.mock_db, "acc1", 150.0)

    async def test_create_transaction_credito(self):
        payload = TransactionIn(
            cuenta_id="acc1",
            tipo="CREDITO",
            monto=50.0,
            descripcion="Retiro"
        )
        
        account_data = {"id": "acc1", "saldo": 200.0, "nombre": "Banco", "codigo": "111"}
        future_acc = asyncio.Future()
        future_acc.set_result(account_data)
        when(self.service.accounts).get(self.mock_db, "acc1").thenReturn(future_acc)
        
        future_update = asyncio.Future()
        future_update.set_result(None)
        # 200 - 50 = 150
        when(self.service.accounts).update_saldo(self.mock_db, "acc1", 150.0).thenReturn(future_update)
        
        tx_data = payload.model_dump()
        tx_data["id"] = "tx1"
        tx_data["fecha"] = "2023-01-01"
        future_tx = asyncio.Future()
        future_tx.set_result(tx_data)
        when(self.service.transactions).create(self.mock_db, mockito_any()).thenReturn(future_tx)
        
        voucher_data = {"id": "v1"}
        future_v = asyncio.Future()
        future_v.set_result(voucher_data)
        when(self.service.vouchers).create(self.mock_db, mockito_any()).thenReturn(future_v)
        
        future_up_tx = asyncio.Future()
        future_up_tx.set_result(None)
        when(self.service.transactions).update(self.mock_db, "tx1", mockito_any()).thenReturn(future_up_tx)
        
        await self.service.create_transaction(self.mock_db, payload)
        
        verify(self.service.accounts).update_saldo(self.mock_db, "acc1", 150.0)

    async def test_create_transaction_account_not_found(self):
        payload = TransactionIn(cuenta_id="acc1", tipo="DEBITO", monto=100.0, descripcion="D")
        
        future_acc = asyncio.Future()
        future_acc.set_result(None)
        when(self.service.accounts).get(self.mock_db, "acc1").thenReturn(future_acc)
        
        with self.assertRaises(HTTPException) as cm:
            await self.service.create_transaction(self.mock_db, payload)
        self.assertEqual(cm.exception.status_code, 404)

    async def test_create_transaction_invalid_type(self):
        payload = TransactionIn(cuenta_id="acc1", tipo="INVALIDO", monto=100.0, descripcion="D")
        
        account_data = {"id": "acc1", "saldo": 50.0}
        future_acc = asyncio.Future()
        future_acc.set_result(account_data)
        when(self.service.accounts).get(self.mock_db, "acc1").thenReturn(future_acc)
        
        with self.assertRaises(HTTPException) as cm:
            await self.service.create_transaction(self.mock_db, payload)
        self.assertEqual(cm.exception.status_code, 400)

    # -----------------
    # Plan de cuentas tests
    # -----------------
    async def test_create_account(self):
        from app.models.chart_account_model import ChartAccountIn
        payload = ChartAccountIn(codigo="1", nombre="Activo", tipo="ACTIVO", saldo=0.0)
        expected = payload.model_dump()
        expected["id"] = "acc1"
        
        future = asyncio.Future()
        future.set_result(expected)
        when(self.service.accounts).create(self.mock_db, mockito_any()).thenReturn(future)
        
        result = await self.service.create_account(self.mock_db, payload)
        self.assertEqual(result.id, "acc1")

    async def test_list_accounts(self):
        acc1 = {"id": "1", "codigo": "1", "nombre": "A", "tipo": "ACTIVO", "saldo": 0.0}
        future = asyncio.Future()
        future.set_result([acc1])
        when(self.service.accounts).list(self.mock_db).thenReturn(future)
        
        result = await self.service.list_accounts(self.mock_db)
        self.assertEqual(len(result), 1)

    async def test_get_account_found(self):
        acc = {"id": "1", "codigo": "1", "nombre": "A", "tipo": "ACTIVO", "saldo": 0.0}
        future = asyncio.Future()
        future.set_result(acc)
        when(self.service.accounts).get(self.mock_db, "1").thenReturn(future)
        
        result = await self.service.get_account(self.mock_db, "1")
        self.assertEqual(result.id, "1")

    async def test_get_account_not_found(self):
        future = asyncio.Future()
        future.set_result(None)
        when(self.service.accounts).get(self.mock_db, "99").thenReturn(future)
        
        with self.assertRaises(HTTPException) as cm:
            await self.service.get_account(self.mock_db, "99")
        self.assertEqual(cm.exception.status_code, 404)

    # -----------------
    # Transacciones tests adicionales
    # -----------------
    async def test_list_transactions(self):
        # Case 1: With comprobante_id
        t1 = {"id": "t1", "cuenta_id": "c1", "monto": 10.0, "tipo": "DEBITO", "comprobante_id": "v1", "descripcion": "d", "fecha": "2023"}
        # Case 2: Without comprobante_id
        t2 = {"id": "t2", "cuenta_id": "c1", "monto": 20.0, "tipo": "CREDITO", "descripcion": "d", "fecha": "2023"}
        
        future = asyncio.Future()
        future.set_result([t1, t2])
        when(self.service.transactions).list(self.mock_db).thenReturn(future)
        
        results = await self.service.list_transactions(self.mock_db)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].comprobante_id, "v1")
        self.assertEqual(results[1].comprobante_id, "PENDING")

    async def test_get_transaction_found(self):
        t1 = {"id": "t1", "cuenta_id": "c1", "monto": 10.0, "tipo": "DEBITO", "descripcion": "d", "fecha": "2023"}
        future = asyncio.Future()
        future.set_result(t1)
        when(self.service.transactions).get(self.mock_db, "t1").thenReturn(future)
        
        result = await self.service.get_transaction(self.mock_db, "t1")
        self.assertEqual(result.id, "t1")
        self.assertEqual(result.comprobante_id, "PENDING")

    async def test_get_transaction_not_found(self):
        future = asyncio.Future()
        future.set_result(None)
        when(self.service.transactions).get(self.mock_db, "t99").thenReturn(future)
        
        with self.assertRaises(HTTPException) as cm:
            await self.service.get_transaction(self.mock_db, "t99")
        self.assertEqual(cm.exception.status_code, 404)

    # -----------------
    # Comprobantes tests
    # -----------------
    async def test_list_vouchers(self):
        v1 = {"id": "v1", "fecha_emision": "2023", "concepto": "c", "transaccion_id": "t1"}
        future = asyncio.Future()
        future.set_result([v1])
        when(self.service.vouchers).list(self.mock_db).thenReturn(future)
        
        result = await self.service.list_vouchers(self.mock_db)
        self.assertEqual(len(result), 1)

    async def test_get_voucher_found(self):
        v1 = {"id": "v1", "fecha_emision": "2023", "concepto": "c", "transaccion_id": "t1"}
        future = asyncio.Future()
        future.set_result(v1)
        when(self.service.vouchers).get(self.mock_db, "v1").thenReturn(future)
        
        result = await self.service.get_voucher(self.mock_db, "v1")
        self.assertEqual(result.id, "v1")

    async def test_get_voucher_not_found(self):
        future = asyncio.Future()
        future.set_result(None)
        when(self.service.vouchers).get(self.mock_db, "v99").thenReturn(future)
        
        with self.assertRaises(HTTPException) as cm:
            await self.service.get_voucher(self.mock_db, "v99")
        self.assertEqual(cm.exception.status_code, 404)
