from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_db
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
async def crear_cuenta(payload: ChartAccountIn, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Crea una nueva cuenta dentro del Plan de Cuentas."""
    return await financial_service.create_account(db, payload)


@router.get("/plan-cuentas", response_model=list[ChartAccountOut], summary="Listar plan de cuentas")
async def listar_cuentas(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Lista las cuentas contables registradas."""
    return await financial_service.list_accounts(db)


@router.get("/plan-cuentas/{account_id}", response_model=ChartAccountOut, summary="Obtener cuenta contable")
async def obtener_cuenta(account_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Obtiene el detalle de una cuenta contable."""
    return await financial_service.get_account(db, account_id)


# -----------------
# Transacciones
# -----------------
@router.post("/transacciones", response_model=TransactionOut, summary="Registrar transacción")
async def registrar_transaccion(payload: TransactionIn, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Registra una transacción y emite su comprobante asociado."""
    return await financial_service.create_transaction(db, payload)


@router.get("/transacciones", response_model=list[TransactionOut], summary="Listar transacciones")
async def listar_transacciones(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Lista las transacciones registradas."""
    return await financial_service.list_transactions(db)


@router.get("/transacciones/{transaction_id}", response_model=TransactionOut, summary="Obtener transacción")
async def obtener_transaccion(transaction_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Obtiene el detalle de una transacción."""
    return await financial_service.get_transaction(db, transaction_id)


# -----------------
# Comprobantes
# -----------------
@router.get("/comprobantes", response_model=list[VoucherOut], summary="Listar comprobantes")
async def listar_comprobantes(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Lista comprobantes emitidos por transacciones."""
    return await financial_service.list_vouchers(db)


@router.get("/comprobantes/{voucher_id}", response_model=VoucherOut, summary="Obtener comprobante")
async def obtener_comprobante(voucher_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Obtiene el detalle de un comprobante."""
    return await financial_service.get_voucher(db, voucher_id)
