from datetime import datetime
import sqlite3

def obtener_folio_diario():
    """
        Genera el siguiente numero de pedido (folio) para el dia actual 

    1. Obtiene fecha actual en formato YY-MM-DD
    2. Busca en la base de datos el folio mas alto registrado SOLO para ese dia
    3. Si no hay registros, empieza en 1
    4. Si si hay, suma +1 al ultimo folio

    ¿Por que se reinicia cada dia?
    
    Porque la consulta SQL filtra por fecha_dia, osea que cada dia es tratado como un conjunto independiente de pedidos
    """

    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    hoy = datetime.now().strftime("%Y-%m-%d")
    #COUNT cuenta registros, DISTINCT folio hace que solo se cuenten valores unicod de la columna folio
    #Resultado cuantos folios diferentes existen y WHERE fecha_dia hace que filtre los registros para que solo considere los que tengan la fecha del dia de hoy
    cursor.execute("""
        SELECT COUNT(DISTINCT folio) FROM ventas WHERE fecha_dia = ?
    """, (hoy, ))

    #Accedemos al primer elemento de la tupla
    count = cursor.fetchone()[0]
    conexion.close()
    #Si tenemos 5 folios, devuelve 6 entonces el unico folio disponible sera 6 despues
    return count + 1



