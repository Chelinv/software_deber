from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

# --------------------------
# Tests para Calificaciones
# --------------------------

@patch("app.api.endpoints.calificaciones_controller.calificaciones_service")
def test_crear_calificacion(mock_service):
    mock_service.create_calificacion = AsyncMock(return_value={
        "id": "c1", "estudiante_id": "e1", "asignatura_id": "a1", 
        "calificacion": 10.0, "fecha_evaluacion": "2023-01-01"
    })
    
    response = client.post("/api/v1/calificaciones/", json={
        "estudiante_id": "e1", "asignatura_id": "a1", 
        "calificacion": 10.0, "fecha_evaluacion": "2023-01-01"
    })
    
    assert response.status_code == 200
    assert response.json()["id"] == "c1"

@patch("app.api.endpoints.calificaciones_controller.calificaciones_service")
def test_crear_calificacion_error(mock_service):
    mock_service.create_calificacion = AsyncMock(side_effect=ValueError("Datos invalidos"))
    
    response = client.post("/api/v1/calificaciones/", json={
        "estudiante_id": "e1", "asignatura_id": "a1", 
        "calificacion": 10.0, "fecha_evaluacion": "2023-01-01"
    })
    
    assert response.status_code == 400

@patch("app.api.endpoints.calificaciones_controller.calificaciones_service")
def test_obtener_calificaciones(mock_service):
    mock_service.get_all_calificaciones = AsyncMock(return_value=[{
        "id": "c1", "estudiante_id": "e1", "asignatura_id": "a1", 
        "calificacion": 10.0, "fecha_evaluacion": "2023-01-01"
    }])
    
    response = client.get("/api/v1/calificaciones/")
    assert response.status_code == 200
    assert len(response.json()) == 1

@patch("app.api.endpoints.calificaciones_controller.calificaciones_service")
def test_obtener_calificacion_por_id(mock_service):
    mock_service.get_calificacion_by_id = AsyncMock(return_value={
        "id": "c1", "estudiante_id": "e1", "asignatura_id": "a1", 
        "calificacion": 10.0, "fecha_evaluacion": "2023-01-01"
    })
    
    response = client.get("/api/v1/calificaciones/c1")
    assert response.status_code == 200
    assert response.json()["id"] == "c1"

@patch("app.api.endpoints.calificaciones_controller.calificaciones_service")
def test_obtener_calificacion_por_id_not_found(mock_service):
    mock_service.get_calificacion_by_id = AsyncMock(side_effect=ValueError("No encontrado"))
    
    response = client.get("/api/v1/calificaciones/c99")
    assert response.status_code == 404

@patch("app.api.endpoints.calificaciones_controller.calificaciones_service")
def test_actualizar_calificacion(mock_service):
    mock_service.update_calificacion = AsyncMock(return_value={
        "id": "c1", "estudiante_id": "e1", "asignatura_id": "a1", 
        "calificacion": 9.0, "fecha_evaluacion": "2023-01-01"
    })
    
    response = client.put("/api/v1/calificaciones/c1", json={
        "estudiante_id": "e1", "asignatura_id": "a1", 
        "calificacion": 9.0, "fecha_evaluacion": "2023-01-01"
    })
    assert response.status_code == 200
    assert response.json()["calificacion"] == 9.0

@patch("app.api.endpoints.calificaciones_controller.calificaciones_service")
def test_eliminar_calificacion(mock_service):
    mock_service.delete_calificacion = AsyncMock(return_value=True)
    
    response = client.delete("/api/v1/calificaciones/c1")
    assert response.status_code == 200
    assert response.json()["exito"] is True


# --------------------------
# Tests para Matrículas
# --------------------------

@patch("app.api.endpoints.matricula_controller.matricula_service")
def test_crear_matricula(mock_service):
    mock_service.create_matricula = AsyncMock(return_value={
        "id": "m1", "estudiante_id": "e1", "asignatura_id": "a1", "fecha_matricula": "2023-01-01"
    })
    
    response = client.post("/api/v1/matriculas/", json={
        "estudiante_id": "e1", "asignatura_id": "a1", "fecha_matricula": "2023-01-01"
    })
    
    assert response.status_code == 200
    assert response.json()["id"] == "m1"

@patch("app.api.endpoints.matricula_controller.matricula_service")
def test_crear_matricula_error(mock_service):
    mock_service.create_matricula = AsyncMock(side_effect=ValueError("Error"))
    
    response = client.post("/api/v1/matriculas/", json={
        "estudiante_id": "e1", "asignatura_id": "a1", "fecha_matricula": "2023-01-01"
    })
    
    assert response.status_code == 400

@patch("app.api.endpoints.matricula_controller.matricula_service")
def test_obtener_matriculas(mock_service):
    mock_service.get_all_matriculas = AsyncMock(return_value=[{
        "id": "m1", "estudiante_id": "e1", "asignatura_id": "a1", "fecha_matricula": "2023-01-01"
    }])
    
    response = client.get("/api/v1/matriculas/")
    assert response.status_code == 200
    assert len(response.json()) == 1

@patch("app.api.endpoints.matricula_controller.matricula_service")
def test_obtener_matricula_por_id(mock_service):
    mock_service.get_matricula_by_id = AsyncMock(return_value={
        "id": "m1", "estudiante_id": "e1", "asignatura_id": "a1", "fecha_matricula": "2023-01-01"
    })
    
    response = client.get("/api/v1/matriculas/m1")
    assert response.status_code == 200
    assert response.json()["id"] == "m1"

@patch("app.api.endpoints.matricula_controller.matricula_service")
def test_actualizar_matricula(mock_service):
    mock_service.update_matricula = AsyncMock(return_value={
        "id": "m1", "estudiante_id": "e1", "asignatura_id": "a1", "fecha_matricula": "2023-01-02"
    })
    
    response = client.put("/api/v1/matriculas/m1", json={
        "estudiante_id": "e1", "asignatura_id": "a1", "fecha_matricula": "2023-01-02"
    })
    assert response.status_code == 200

@patch("app.api.endpoints.matricula_controller.matricula_service")
def test_eliminar_matricula(mock_service):
    mock_service.delete_matricula = AsyncMock(return_value=True)
    
    response = client.delete("/api/v1/matriculas/m1")
    assert response.status_code == 200
    assert response.json()["eliminado"] is True
