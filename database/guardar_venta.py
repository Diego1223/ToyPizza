import sqlite3
from datetime import datetime

def guardar_venta_folio(pizza, folio):
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    fecha_dia = ahora.strftime("%Y-%m-%d")

    if pizza["tipo"] == "mitad":
        ingredientes = f"{','.join(pizza['lado1'])} / {','.join(pizza['lado2'])}"
    else:
        ingredientes = ",".join(pizza["ingredientes"])

    cursor.execute("""
        INSERT INTO ventas (folio, fecha, fecha_dia, tamano, tipo, ingredientes, precio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        folio,
        fecha,
        fecha_dia,
        pizza["tamano"],
        pizza["tipo"],
        ingredientes,
        pizza["precio"]
    ))

    conexion.commit()
    conexion.close()