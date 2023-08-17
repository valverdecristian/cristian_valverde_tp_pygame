import sqlite3

lista = list()

with sqlite3.connect("mi_base_de_datos.db") as conexion:
    try:
        sentencia = '''
                    select * from Ranking order by score desc limit 3
                    '''
        cursor = conexion.execute(sentencia)
        for fila in cursor:
            lista.append(fila)

        print("Tabla creada")
        
    except Exception as e:
        print(f"Error en Base de datos {e}")
        
print(lista)