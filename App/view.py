import sys
import App.logic as l
from tabulate import tabulate

def new_logic():
    """
        Se crea una instancia del controlador
    """
    catalog = l.new_logic()
    return catalog

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    filename = input("Ingrese el nombre del archivo: ")
    catalog, tiempo, total, primeros, ultimos = l.load_data(control, filename)
    
    print("\n" + "="*100)
    print(" "*35 + "REPORTE DE CARGA DE DATOS")
    print("="*100)
    print(f"\nTiempo de carga: {tiempo:.2f} ms")
    print(f"Total de vuelos cargados: {total:,}")
    
    # Preparar datos de los primeros 5 vuelos para tabulate
    print("\n" + "-"*100)
    print(" "*30 + "PRIMEROS 5 VUELOS (Orden Cronológico)")
    print("-"*100)
    
    tabla_primeros = []
    for vuelo in primeros:
        tabla_primeros.append([
            vuelo['fecha'],
            vuelo['hora_salida'],
            vuelo['hora_llegada'],
            f"{vuelo['codigo_aerolinea']}\n{vuelo['nombre_aerolinea']}",
            vuelo['aeronave'],
            f"{vuelo['origen']}\n→ {vuelo['destino']}",
            f"{vuelo['duracion_min']} min",
            f"{vuelo['distancia_millas']} mi"
        ])
    
    headers_primeros = ["Fecha", "Salida", "Llegada", "Aerolínea", "Aeronave", "Ruta", "Duración", "Distancia"]
    print(tabulate(tabla_primeros, headers=headers_primeros, tablefmt="fancy_grid", stralign="center"))
    
    # Preparar datos de los últimos 5 vuelos para tabulate
    print("\n" + "-"*100)
    print(" "*30 + "ÚLTIMOS 5 VUELOS (Orden Cronológico)")
    print("-"*100)
    
    tabla_ultimos = []
    for vuelo in ultimos:
        tabla_ultimos.append([
            vuelo['fecha'],
            vuelo['hora_salida'],
            vuelo['hora_llegada'],
            f"{vuelo['codigo_aerolinea']}\n{vuelo['nombre_aerolinea']}",
            vuelo['aeronave'],
            f"{vuelo['origen']}\n→ {vuelo['destino']}",
            f"{vuelo['duracion_min']} min",
            f"{vuelo['distancia_millas']} mi"
        ])
    
    headers_ultimos = ["Fecha", "Salida", "Llegada", "Aerolínea", "Aeronave", "Ruta", "Duración", "Distancia"]
    print(tabulate(tabla_ultimos, headers=headers_ultimos, tablefmt="fancy_grid", stralign="center"))
    
    print("\n" + "="*100)
    
    return catalog, tiempo, total, primeros, ultimos



def print_data(control, id):

    id = input("Ingrese el indice del dato a consultar: ")
    print(l.get_data(control, id))

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
