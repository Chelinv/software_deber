# app/models/transaction_model.py
from datetime import datetime
from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    """Esquema base para Transacciones."""

    fecha: datetime = Field(default_factory=datetime.utcnow)
    descripcion: str = Field(..., examples=["Pago de matrícula"])
    monto: float = Field(..., gt=0, examples=[120.0])
    tipo: str = Field(..., description="DEBITO | CREDITO", examples=["DEBITO"])
    cuenta_id: int = Field(..., examples=[1])


class TransactionIn(TransactionBase):
    """Entrada para registrar una transacción."""

    pass


class TransactionOut(TransactionBase):
    """Salida de transacción."""

    id: int
    comprobante_id: int

    class Config:
        from_attributes = True
