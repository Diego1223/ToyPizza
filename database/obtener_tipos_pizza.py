import sqlite3

def obtener_tipos_pizza():
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre FROM tipos_pizza")

    tipos = cursor.fetchall()

    conexion.close()
    
    #COnvertir los valores a una lista
    return [t[0] for t in tipos]