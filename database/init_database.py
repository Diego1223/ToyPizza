import sqlite3

def init_db():
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folio INTEGER,
        fecha TEXT,
        fecha_dia TEXT,
        tamano TEXT,
        tipo TEXT,
        ingredientes TEXT,
        precio INTEGER
    )
    """)

    conexion.commit()
    conexion.close()  
