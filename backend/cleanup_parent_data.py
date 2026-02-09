"""
Script para limpiar la base de datos eliminando:
1. Colección relaciones_padre_hijo
2. Usuarios con rol "Padre"
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.database import client

async def cleanup_parent_data():
    """Elimina todos los datos relacionados con el rol Padre"""
    try:
        db = client["gestion_educativa"]
        
        print("=" * 70)
        print("LIMPIEZA DE DATOS DE PADRE")
        print("=" * 70)
        
        # 1. Eliminar colección relaciones_padre_hijo
        print("\n[1] Eliminando colección 'relaciones_padre_hijo'...")
        try:
            await db.drop_collection("relaciones_padre_hijo")
            print("    OK - Colección eliminada")
        except Exception as e:
            print(f"    INFO - {e}")
        
        # 2. Contar usuarios con rol Padre
        print("\n[2] Buscando usuarios con rol 'Padre'...")
        padre_count = await db.usuarios.count_documents({"rol": "Padre"})
        print(f"    Encontrados: {padre_count} usuarios")
        
        if padre_count > 0:
            # Mostrar usuarios que serán eliminados
            padres = await db.usuarios.find({"rol": "Padre"}).to_list(length=100)
            print("\n    Usuarios que serán eliminados:")
            for padre in padres:
                print(f"    - {padre.get('nombre', 'N/A')} ({padre.get('email', 'N/A')})")
            
            # Eliminar usuarios con rol Padre
            print("\n[3] Eliminando usuarios con rol 'Padre'...")
            result = await db.usuarios.delete_many({"rol": "Padre"})
            print(f"    OK - {result.deleted_count} usuarios eliminados")
        else:
            print("    No hay usuarios con rol 'Padre' para eliminar")
        
        print("\n" + "=" * 70)
        print("LIMPIEZA COMPLETADA")
        print("=" * 70)
        print("\nResumen:")
        print("- Colección 'relaciones_padre_hijo' eliminada")
        print(f"- {padre_count} usuarios con rol 'Padre' eliminados")
        print("\nRoles disponibles ahora:")
        print("- Administrador")
        print("- Docente")
        print("- Estudiante")
        
    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(cleanup_parent_data())
