import sqlite3

def obtener_tamanos():
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre FROM tamanos")

    tamanos = cursor.fetchall()
    conexion.close()
    
    #Convertimos el resultado en lista
    return [t[0] for t in tamanos]

