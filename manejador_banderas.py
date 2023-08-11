import json

def crear_banderas(banderas_niveles):
    """
    La función "crear_banderas" crea un archivo JSON llamado "Banderas_Niveles.json" y escribe en él el
    contenido de la variable "banderas_niveles".
    
    :param banderas_niveles: El parámetro "banderas_niveles" es un diccionario que contiene la
    información sobre las banderas y niveles
    """
    with open("Banderas_Niveles.json", "w") as archivo:
        json.dump(banderas_niveles, archivo)

def leer_banderas():
    """
    La función "leer_banderas" lee el contenido de un archivo JSON llamado "Banderas_Niveles.json" y lo
    almacena en la variable "banderas_niveles".

    """
    with open("Banderas_Niveles.json", "r") as archivo:
        banderas_niveles = json.load(archivo)

def modificar_banderas(nivel, bandera, nuevo_valor):
    """
    La función `modificar_banderas` modifica el valor de una bandera ("terminado" o "reset") para un nivel dado en un archivo JSON.

    :param nivel: El nivel al que se le modificará la bandera.
    :param bandera: La bandera que se desea modificar ("terminado" o "reset").
    :param nuevo_valor: El nuevo valor para la bandera especificada.
    """
    with open("Banderas_Niveles.json", "r") as archivo:
        banderas_niveles = json.load(archivo)

    banderas_niveles[nivel][bandera] = nuevo_valor

    with open("Banderas_Niveles.json", "w") as archivo:
        json.dump(banderas_niveles, archivo)

# Ejemplo de uso:
# Supongamos que quieres modificar la bandera "terminado" del nivel 1 a True.
modificar_banderas(1, "terminado", True)

# Ahora, si quieres modificar la bandera "reset" del nivel 2 a False, puedes hacer lo siguiente:
modificar_banderas(2, "reset", False)
