import sqlite3

def ver():
    conexion = sqlite3.connect("ventas.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM ventas")
    resultados = cursor.fetchall()

    for fila in resultados:
        print(fila)
    
    conexion.close()

ver()
