"""
Script para hashear contraseñas en texto plano en la base de datos
Ejecutar este script después de cambiar contraseñas desde el admin
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from bson import ObjectId

# Configuración
MONGO_URI = "mongodb+srv://chelinv:Celine2005@cluster0.5ygxk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "gestion_educativa"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def fix_plain_text_passwords():
    """
    Encuentra y hashea todas las contraseñas en texto plano
    """
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    try:
        print("Conectando a MongoDB...")
        usuarios = await db.usuarios.find().to_list(length=None)
        print(f"Encontrados {len(usuarios)} usuarios")
        
        fixed_count = 0
        for usuario in usuarios:
            password = usuario.get("password", "")
            
            # Verificar si la contraseña NO está hasheada
            # Las contraseñas hasheadas con bcrypt empiezan con $2b$
            if password and not password.startswith("$2b$"):
                print(f"\nUsuario: {usuario.get('nombre')} ({usuario.get('email')})")
                print(f"  Contraseña en texto plano detectada: {password[:3]}***")
                
                # Hashear la contraseña
                hashed_password = pwd_context.hash(password)
                
                # Actualizar en la base de datos
                result = await db.usuarios.update_one(
                    {"_id": ObjectId(usuario["_id"])},
                    {"$set": {"password": hashed_password}}
                )
                
                if result.modified_count > 0:
                    print(f"  ✅ Contraseña hasheada correctamente")
                    fixed_count += 1
                else:
                    print(f"  ❌ Error al actualizar")
        
        print(f"\n{'='*50}")
        print(f"Proceso completado:")
        print(f"  Total usuarios: {len(usuarios)}")
        print(f"  Contraseñas corregidas: {fixed_count}")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("="*50)
    print("SCRIPT: Corrección de Contraseñas en Texto Plano")
    print("="*50)
    asyncio.run(fix_plain_text_passwords())
