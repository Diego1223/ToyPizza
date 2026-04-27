import sqlite3

def calcular_precio(pizza):
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    # -----------------------
    # TAMAÑO
    # -----------------------
    cursor.execute("""
        SELECT precio_base, precio_extra, extra_mitad
        FROM tamanos
        WHERE LOWER(nombre) = LOWER(?)
    """, (pizza["tamano"],))

    row = cursor.fetchone()
    
    if not row:
        print("❌ Tamaño no encontrado:", pizza["tamano"])
        return 0
    
    base, extra_completa, extra_mitad = row
    total = base

    # -----------------------
    # TIPO DE PIZZA
    # -----------------------
    cursor.execute("""
        SELECT precio
        FROM precios_tipos_pizza
        WHERE tipo_id = (
            SELECT id FROM tipos_pizza WHERE nombre = ?
        )
        AND LOWER(tamano) = LOWER(?)
    """, (pizza["tipo_base"], pizza["tamano"]))

    tipo_row = cursor.fetchone()

    if tipo_row:
        total += tipo_row[0]
    else:
        print("⚠️ Tipo sin precio:", pizza["tipo_base"], pizza["tamano"])

    # -----------------------
    # INGREDIENTES
    # -----------------------
    if pizza["tipo"] == "mitad":
        ingredientes = pizza["lado1"] + pizza["lado2"]
        ingredientes_gratis = 2
        precio_extra = extra_mitad
    else:
        ingredientes = pizza["ingredientes"]
        ingredientes_gratis = 1
        precio_extra = extra_completa

    extras = max(0, len(ingredientes) - ingredientes_gratis)

    total += extras * precio_extra

    conexion.close()
    return total