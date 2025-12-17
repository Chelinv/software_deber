# app/repositories/voucher_repository.py


class VoucherRepository:
    """Repositorio en memoria para Comprobantes."""

    def __init__(self):
        self._data: dict[int, dict] = {}
        self._seq: int = 1

    def create(self, payload: dict) -> dict:
        payload = payload.copy()
        payload["id"] = self._seq
        self._data[self._seq] = payload
        self._seq += 1
        return payload

    def get(self, voucher_id: int) -> dict | None:
        return self._data.get(voucher_id)

    def list(self) -> list[dict]:
        return list(self._data.values())
