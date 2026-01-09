from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    # La ruta raiz ahora redirecciona
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"

def test_docs_accessible():
    response = client.get("/docs")
    assert response.status_code == 200

# Más pruebas de integración requerirían mockear la base de datos
# para no depender de una instancia real de MongoDB.
