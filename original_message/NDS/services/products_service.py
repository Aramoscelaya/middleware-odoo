# Ej. obtener, crear, validar usuarios
#from ...database import init_db
#import mysql.connector
#from models.products_model import Products
from middleware.logger import get_logger
from original_message.models import original_message
from typing import Dict, Any

logger = get_logger("Products Service", "logs/sync.log")

def create_maintenances(data):
    response = []
    try:
        DB_CONECT = init_db()
        cursor = DB_CONECT.cursor()

        productSearch = product_by_serialnumber(data['default_code'])

        if not productSearch:
            logger.warning("Producto no encontrado")
        else:
            msj = ""
            try:
                sql = 'INSERT INTO mantenimientos (estado_manto, descripcion_manto, estatus, id_producto, usuario_modificacion) VALUES (%s, %s, %s, %s, %s)'
                valores = ([int(data['estado_manto']), data['descripcion_manto'], 1, productSearch[0][0], 'Admin'])
                cursor.execute(sql, valores)
                DB_CONECT.commit()  # Guarda los cambios en la base de datos

                if cursor.rowcount > 0:
                    msj = "✅ Mantenimiento agregado"
                else:
                    msj = "⚠️ Mantenimiento no generado"

            except mysql.connector.Error as err:
                print("❌ Error de MySQL:", err)

            DB_CONECT.close()
            return msj
    except mysql.connector.errors.ProgrammingError as e:
        logger.error("Error conectando a MySQL: %s", e)
        print(f"Error en la consulta SQL: {e}")
    except mysql.connector.Error as e:
        print(f"⚠️ Error en la conexión o ejecución: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexion' in locals() and DB_CONECT.is_connected():
            DB_CONECT.close()
            print("Conexión cerrada.")
    
    return response

def product_by_serialnumber(serialNumber):
    datos = []
    try:
        DB_CONECT = init_db()
        cursor = DB_CONECT.cursor()

        cursor.execute(f"SELECT * FROM products WHERE default_code = '{serialNumber}'")
        datos = cursor.fetchall()  # Obtiene todos los registros
        DB_CONECT.close()

    except mysql.connector.errors.ProgrammingError as e:
        print(f"❌ Error en la consulta SQL: {e}")
    except mysql.connector.Error as e:
        print(f"⚠️ Error en la conexión o ejecución: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexion' in locals() and DB_CONECT.is_connected():
            DB_CONECT.close()
            print("Conexión cerrada.")
    
    return datos

def guardar_o_actualizar_producto(data: Dict[str, Any]) -> Dict[str, Any]:
    producto, creado = original_message.objects.create(
        file = data[0],
        entity = data[1],
        status = data[2],
        request = data[3],
    )

    if creado:
        print(f"✅ Producto creado: {producto.codigo} - {producto.nombre}")
    else:
        print(f"🔄 Producto actualizado: {producto.codigo} - {producto.nombre}")

    return producto

