# app/models/chart_account_model.py
from pydantic import BaseModel, Field


class ChartAccountBase(BaseModel):
    """Esquema base para Plan de Cuentas."""

    codigo: str = Field(..., examples=["1.1.01"])
    nombre: str = Field(..., examples=["Caja"])
    tipo: str = Field(
        ..., description="ACTIVO | PASIVO | PATRIMONIO | INGRESO | GASTO", examples=["ACTIVO"]
    )
    descripcion: str | None = Field(default=None, examples=["Cuenta principal de efectivo"])


class ChartAccountIn(ChartAccountBase):
    """Entrada para crear/editar cuenta."""

    pass


class ChartAccountOut(ChartAccountBase):
    """Salida de cuenta."""

    id: int
    saldo: float = Field(default=0.0, examples=[150.75])

    class Config:
        from_attributes = True
