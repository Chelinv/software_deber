# app/api/endpoints/financial_controller.py
from fastapi import APIRouter

from app.models.chart_account_model import ChartAccountIn, ChartAccountOut
from app.models.transaction_model import TransactionIn, TransactionOut
from app.models.voucher_model import VoucherOut
from app.services.financial_service import FinancialService


router = APIRouter()
financial_service = FinancialService()


# -----------------
# Plan de cuentas
# -----------------
@router.post("/plan-cuentas", response_model=ChartAccountOut, summary="Crear cuenta contable")
def crear_cuenta(payload: ChartAccountIn):
    """Crea una nueva cuenta dentro del Plan de Cuentas."""
    return financial_service.create_account(payload)


@router.get("/plan-cuentas", response_model=list[ChartAccountOut], summary="Listar plan de cuentas")
def listar_cuentas():
    """Lista las cuentas contables registradas."""
    return financial_service.list_accounts()


@router.get("/plan-cuentas/{account_id}", response_model=ChartAccountOut, summary="Obtener cuenta contable")
def obtener_cuenta(account_id: int):
    """Obtiene el detalle de una cuenta contable."""
    return financial_service.get_account(account_id)


# -----------------
# Transacciones
# -----------------
@router.post("/transacciones", response_model=TransactionOut, summary="Registrar transacción")
def registrar_transaccion(payload: TransactionIn):
    """Registra una transacción y emite su comprobante asociado."""
    return financial_service.create_transaction(payload)


@router.get("/transacciones", response_model=list[TransactionOut], summary="Listar transacciones")
def listar_transacciones():
    """Lista las transacciones registradas."""
    return financial_service.list_transactions()


@router.get("/transacciones/{transaction_id}", response_model=TransactionOut, summary="Obtener transacción")
def obtener_transaccion(transaction_id: int):
    """Obtiene el detalle de una transacción."""
    return financial_service.get_transaction(transaction_id)


# -----------------
# Comprobantes
# -----------------
@router.get("/comprobantes", response_model=list[VoucherOut], summary="Listar comprobantes")
def listar_comprobantes():
    """Lista comprobantes emitidos por transacciones."""
    return financial_service.list_vouchers()


@router.get("/comprobantes/{voucher_id}", response_model=VoucherOut, summary="Obtener comprobante")
def obtener_comprobante(voucher_id: int):
    """Obtiene el detalle de un comprobante."""
    return financial_service.get_voucher(voucher_id)
