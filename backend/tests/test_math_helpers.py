import pytest
from app.utils.math_helpers import calcular_promedio, es_aprobado

def test_calcular_promedio():
    assert calcular_promedio([10, 8, 9]) == 9.0
    assert calcular_promedio([]) == 0.0

def test_es_aprobado():
    assert es_aprobado(8.0) is True
    assert es_aprobado(6.0) is False
