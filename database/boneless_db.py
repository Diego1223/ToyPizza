import sqlite3

def get_boneless():
    try:
        conexion = sqlite3.connect("ventas.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT nombre, precio_base, salsas_gratis, precio_extra_salsa FROM boneless")
        
        rows = cursor.fetchall()
        conexion.close()

        return [
            {
                "nombre": row[0],
                "precio_base": row[1],
                "salsas_gratis": row[2],
                "precio_extra_salsa": row[3]
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error {e}")

def get_salsas():
    try:
        conexion = sqlite3.connect("ventas.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT nombre FROM salsas_boneless")
        
        rows = cursor.fetchall()
        conexion.close()

        return [
            {
                "nombre": row[0]
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error {e}")