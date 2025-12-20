from motor.motor_asyncio import AsyncIOMotorClient
import certifi

# URI de MongoDB Atlas
MONGO_URI = "mongodb+srv://chelinv2004_db_user:5pNP7PffKUcTubBb@cluster0.q5s0hpk.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"

# Cliente Mongo
# La configuración de TLS se maneja en la URI
client = AsyncIOMotorClient(MONGO_URI)

# Base de datos
database = client.sgie  # nombre de la BD

# Dependencia para FastAPI
def get_db():
    return database
