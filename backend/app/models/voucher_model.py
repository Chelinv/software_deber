# app/models/voucher_model.py
from datetime import datetime
from pydantic import BaseModel, Field


class VoucherBase(BaseModel):
    """Esquema base para Comprobantes."""

    fecha_emision: datetime = Field(default_factory=datetime.utcnow)
    concepto: str = Field(..., examples=["Comprobante de transacción"])


class VoucherOut(VoucherBase):
    """Salida de comprobante."""

    id: str
    transaccion_id: str

    class Config:
        from_attributes = True
