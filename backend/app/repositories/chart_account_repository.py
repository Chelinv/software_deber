# app/repositories/chart_account_repository.py


class ChartAccountRepository:
    """Repositorio en memoria para Plan de Cuentas (mínimo evaluable)."""

    def __init__(self):
        self._data: dict[int, dict] = {}
        self._seq: int = 1

    def create(self, payload: dict) -> dict:
        payload = payload.copy()
        payload["id"] = self._seq
        payload.setdefault("saldo", 0.0)
        self._data[self._seq] = payload
        self._seq += 1
        return payload

    def get(self, account_id: int) -> dict | None:
        return self._data.get(account_id)

    def list(self) -> list[dict]:
        return list(self._data.values())

    def update_saldo(self, account_id: int, nuevo_saldo: float) -> dict | None:
        acc = self._data.get(account_id)
        if not acc:
            return None
        acc["saldo"] = float(nuevo_saldo)
        return acc
