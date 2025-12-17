from datetime import datetime
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.chart_account_model import ChartAccountIn, ChartAccountOut
from app.models.transaction_model import TransactionIn, TransactionOut
from app.models.voucher_model import VoucherOut
from app.repositories.chart_account_repository import ChartAccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.voucher_repository import VoucherRepository


class FinancialService:
    """Lógica de negocio para Transacciones/Comprobantes/Plan de Cuentas."""

    def __init__(self):
        self.accounts = ChartAccountRepository()
        self.transactions = TransactionRepository()
        self.vouchers = VoucherRepository()

    # -----------------
    # Plan de cuentas
    # -----------------
    async def create_account(self, db: AsyncIOMotorDatabase, payload: ChartAccountIn) -> ChartAccountOut:
        created = await self.accounts.create(db, payload.model_dump())
        return ChartAccountOut(**created)

    async def list_accounts(self, db: AsyncIOMotorDatabase) -> list[ChartAccountOut]:
        accounts = await self.accounts.list(db)
        return [ChartAccountOut(**a) for a in accounts]

    async def get_account(self, db: AsyncIOMotorDatabase, account_id: str) -> ChartAccountOut:
        acc = await self.accounts.get(db, account_id)
        if not acc:
            raise HTTPException(status_code=404, detail="Cuenta contable no encontrada")
        return ChartAccountOut(**acc)

    # -----------------
    # Transacciones
    # -----------------
    async def create_transaction(self, db: AsyncIOMotorDatabase, payload: TransactionIn) -> TransactionOut:
        acc = await self.accounts.get(db, payload.cuenta_id)
        if not acc:
            raise HTTPException(status_code=404, detail="Cuenta contable no encontrada")

        # Ajuste simple de saldo
        saldo_actual = float(acc.get("saldo", 0.0))
        if payload.tipo.upper() == "DEBITO":
            saldo_nuevo = saldo_actual + payload.monto
        elif payload.tipo.upper() == "CREDITO":
            saldo_nuevo = saldo_actual - payload.monto
        else:
            raise HTTPException(status_code=400, detail="tipo debe ser DEBITO o CREDITO")

        await self.accounts.update_saldo(db, payload.cuenta_id, saldo_nuevo)

        # Crear transacción
        tx_dict = payload.model_dump()
        tx_dict["fecha"] = tx_dict.get("fecha") or datetime.utcnow()
        tx_created = await self.transactions.create(db, tx_dict)

        # Emitir comprobante
        v_created = await self.vouchers.create(db, 
            {
                "fecha_emision": datetime.utcnow(),
                "concepto": f"Comprobante: {payload.descripcion}",
                "transaccion_id": tx_created["id"],
            }
        )

        # Enlazar y actualizar transacción
        await self.transactions.update(db, tx_created["id"], {"comprobante_id": v_created["id"]})
        
        tx_created["comprobante_id"] = v_created["id"]
        return TransactionOut(**tx_created)

    async def list_transactions(self, db: AsyncIOMotorDatabase) -> list[TransactionOut]:
        transactions = await self.transactions.list(db)
        results = []
        for t in transactions:
            if "comprobante_id" not in t:
                t["comprobante_id"] = "PENDING"
            results.append(TransactionOut(**t))
        return results

    async def get_transaction(self, db: AsyncIOMotorDatabase, transaction_id: str) -> TransactionOut:
        tx = await self.transactions.get(db, transaction_id)
        if not tx:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        if "comprobante_id" not in tx:
            tx["comprobante_id"] = "PENDING"
        return TransactionOut(**tx)
        
    # -----------------
    # Comprobantes
    # -----------------
    async def list_vouchers(self, db: AsyncIOMotorDatabase) -> list[VoucherOut]:
        vouchers = await self.vouchers.list(db)
        return [VoucherOut(**v) for v in vouchers]

    async def get_voucher(self, db: AsyncIOMotorDatabase, voucher_id: str) -> VoucherOut:
        v = await self.vouchers.get(db, voucher_id)
        if not v:
            raise HTTPException(status_code=404, detail="Comprobante no encontrado")
        return VoucherOut(**v)
