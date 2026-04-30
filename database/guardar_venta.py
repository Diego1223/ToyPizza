import sqlite3
from datetime import datetime


#El folio sigue siendo el mismo cuando es complemento porque PERTENECE A LA MISMA VENTA
def guardar_venta_folio(item, folio):
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    fecha_dia = ahora.strftime("%Y-%m-%d")

    if item.get("tipo_item") == "complemento":
        cursor.execute("""
            INSERT INTO detalle_complementos (
                folio,
                fecha,
                fecha_dia,
                nombre,
                cantidad,
                precio
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            folio,
            fecha,
            fecha_dia,
            item["nombre"],
            item["cantidad"],
            item["precio"]
        ))
    else:

        if item["tipo"] == "mitad":
            ingredientes = f"{','.join(item['lado1'])} / {','.join(item['lado2'])}"
        else:
            ingredientes = ",".join(item["ingredientes"])

        cursor.execute("""
            INSERT INTO ventas (folio, fecha, fecha_dia, tamano, tipo, ingredientes, precio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            folio,
            fecha,
            fecha_dia,
            item["tamano"],
            item["tipo"],
            ingredientes,
            item["precio"]
        ))
    
    return folio, fecha_dia, item,
    conexion.commit()
    conexion.close()