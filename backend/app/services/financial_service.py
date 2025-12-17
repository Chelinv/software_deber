# app/services/financial_service.py
from datetime import datetime
from fastapi import HTTPException

from app.models.chart_account_model import ChartAccountIn, ChartAccountOut
from app.models.transaction_model import TransactionIn, TransactionOut
from app.models.voucher_model import VoucherOut
from app.repositories.chart_account_repository import ChartAccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.voucher_repository import VoucherRepository


class FinancialService:
    """Lógica de negocio para Transacciones/Comprobantes/Plan de Cuentas (mínimo evaluable).

    Nota: Se implementa en memoria para cumplir el deber sin depender de BD.
    """

    def __init__(self):
        self.accounts = ChartAccountRepository()
        self.transactions = TransactionRepository()
        self.vouchers = VoucherRepository()

        # Cuentas base de ejemplo (para que el Swagger tenga data rápida)
        self._seed_if_empty()

    def _seed_if_empty(self) -> None:
        if self.accounts.list():
            return
        self.accounts.create(
            {
                "codigo": "1.1.01",
                "nombre": "Caja",
                "tipo": "ACTIVO",
                "descripcion": "Cuenta de efectivo",
                "saldo": 0.0,
            }
        )

    # -----------------
    # Plan de cuentas
    # -----------------
    def create_account(self, payload: ChartAccountIn) -> ChartAccountOut:
        created = self.accounts.create(payload.model_dump())
        return ChartAccountOut(**created)

    def list_accounts(self) -> list[ChartAccountOut]:
        return [ChartAccountOut(**a) for a in self.accounts.list()]

    def get_account(self, account_id: int) -> ChartAccountOut:
        acc = self.accounts.get(account_id)
        if not acc:
            raise HTTPException(status_code=404, detail="Cuenta contable no encontrada")
        return ChartAccountOut(**acc)

    # -----------------
    # Transacciones
    # -----------------
    def create_transaction(self, payload: TransactionIn) -> TransactionOut:
        acc = self.accounts.get(payload.cuenta_id)
        if not acc:
            raise HTTPException(status_code=404, detail="Cuenta contable no encontrada")

        # Ajuste simple de saldo (mínimo evaluable)
        saldo_actual = float(acc.get("saldo", 0.0))
        if payload.tipo.upper() == "DEBITO":
            saldo_nuevo = saldo_actual + payload.monto
        elif payload.tipo.upper() == "CREDITO":
            saldo_nuevo = saldo_actual - payload.monto
        else:
            raise HTTPException(status_code=400, detail="tipo debe ser DEBITO o CREDITO")

        self.accounts.update_saldo(payload.cuenta_id, saldo_nuevo)

        # Crear transacción
        tx_dict = payload.model_dump()
        tx_dict["fecha"] = tx_dict.get("fecha") or datetime.utcnow()
        tx_created = self.transactions.create(tx_dict)

        # Emitir comprobante
        v_created = self.vouchers.create(
            {
                "fecha_emision": datetime.utcnow(),
                "concepto": f"Comprobante: {payload.descripcion}",
                "transaccion_id": tx_created["id"],
            }
        )

        # Enlazar
        tx_created["comprobante_id"] = v_created["id"]
        return TransactionOut(**tx_created)

    def list_transactions(self) -> list[TransactionOut]:
        return [TransactionOut(**t) for t in self.transactions.list()]

    def get_transaction(self, transaction_id: int) -> TransactionOut:
        tx = self.transactions.get(transaction_id)
        if not tx:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        return TransactionOut(**tx)

    # -----------------
    # Comprobantes
    # -----------------
    def list_vouchers(self) -> list[VoucherOut]:
        return [VoucherOut(**v) for v in self.vouchers.list()]

    def get_voucher(self, voucher_id: int) -> VoucherOut:
        v = self.vouchers.get(voucher_id)
        if not v:
            raise HTTPException(status_code=404, detail="Comprobante no encontrado")
        return VoucherOut(**v)
