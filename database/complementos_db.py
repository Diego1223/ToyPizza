import sqlite3

def complementos_db():
    try:
        conexion = sqlite3.connect("ventas.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT nombre, precio FROM complementos")

        rows = cursor.fetchall()
        conexion.close()

        return [
            {
                "nombre": row[0],
                "precio": row[1]
            }
            for row in rows
        ]

    except Exception as e:
        print("Algo fallo")