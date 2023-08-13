import json

def crear_banderas(banderas_niveles):
    """
    La función "crear_banderas" crea un archivo JSON llamado "Banderas_Niveles.json" y escribe en él el
    contenido de la variable "banderas_niveles".
    
    :param banderas_niveles: El parámetro "banderas_niveles" es un diccionario que contiene la
    información sobre las banderas y niveles
    """
    with open('banderas_niveles.json', 'w') as archivo:
        json.dump(banderas_niveles, archivo, indent=4)


def leer_bandera(nivel, bandera):
    """
    La función `leer_bandera` lee el valor de una bandera ("terminado" o "reset") para un nivel dado en un archivo JSON.

    :param nivel: El nivel del que se leerá la bandera.
    :param bandera: La bandera que se desea leer ("terminado" o "reset").
    :return: El valor de la bandera especificada.
    """
    with open("Banderas_Niveles.json", "r") as archivo:
        banderas_niveles = json.load(archivo)

    return banderas_niveles[nivel][bandera]

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
        json.dump(banderas_niveles, archivo, indent=4)
