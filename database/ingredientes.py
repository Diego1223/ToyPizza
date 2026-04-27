import sqlite3

def obtener_ingredientes():
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre FROM ingredientes")

    resultado = cursor.fetchall()
    
    #convertir [('Peperoni', ), ('Jamon',)] a ['Peperoni', 'Jamon']
    return [r[0] for r in resultado]