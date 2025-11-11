import sys
import App.logic as l
from tabulate import tabulate
from DataStructures.List import array_list as al

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
    """
    Función que imprime la solución del Requerimiento 1 en consola
    """
    print("\n" + "="*100)
    print(" "*25 + "REQUERIMIENTO 1: VUELOS CON RETRASO EN SALIDA")
    print("="*100)
    
    # Solicitar datos de entrada
    code = input("\nIngrese el código de la aerolínea (ej: UA): ").strip().upper()
    
    try:
        min_delay = float(input("Ingrese el retraso mínimo en minutos: "))
        max_delay = float(input("Ingrese el retraso máximo en minutos: "))
    except ValueError:
        print("Error: Debe ingresar valores numéricos válidos.")
        return
    
    if min_delay > max_delay:
        print("Error: El retraso mínimo no puede ser mayor que el máximo.")
        return

    tiempo, total, primeros, ultimos = l.req_1(control, code, min_delay, max_delay)
    
    # Mostrar resultados
    print("\n" + "-"*100)
    print("RESULTADOS")
    print("-"*100)
    print(f"Tiempo de ejecución: {tiempo:.2f} ms")
    print(f"Total de vuelos encontrados: {total:,}")
    print(f"Aerolínea: {code}")
    print(f"Rango de retraso: [{min_delay}, {max_delay}] minutos")
    
    if total == 0:
        print("\nNo se encontraron vuelos que cumplan con los criterios especificados.")
        print("="*100 + "\n")
        return
    
    # Mostrar primeros 5 vuelos
    if al.size(primeros) > 0:
        print("\n" + "-"*100)
        if total <= 10:
            print(" "*35 + f"TODOS LOS VUELOS ({total})")
        else:
            print(" "*35 + "PRIMEROS 5 VUELOS")
        print("-"*100)
        
        tabla_primeros = []
        for i in range(al.size(primeros)):
            vuelo = al.get_element(primeros, i)
            tabla_primeros.append([
                vuelo['id_vuelo'],
                vuelo['codigo_vuelo'],
                vuelo['fecha'],
                vuelo['codigo_aerolinea'],
                vuelo['nombre_aerolinea'],
                vuelo['aeropuerto_origen'],
                vuelo['aeropuerto_destino'],
                f"{vuelo['retraso_min']:+.2f}"  # El + muestra el signo
            ])
        
        headers = ["ID", "Código\nVuelo", "Fecha", "Cód.\nAerolínea", "Nombre Aerolínea", 
                   "Origen", "Destino", "Retraso\n(min)"]
        print(tabulate(tabla_primeros, headers=headers, tablefmt="grid"))
    
    # Mostrar últimos 5 vuelos si hay más de 10
    if al.size(ultimos) > 0 and total > 10:
        print("\n" + "-"*100)
        print(" "*35 + "ÚLTIMOS 5 VUELOS")
        print("-"*100)
        
        tabla_ultimos = []
        for i in range(al.size(ultimos)):
            vuelo = al.get_element(ultimos, i)
            tabla_ultimos.append([
                vuelo['id_vuelo'],
                vuelo['codigo_vuelo'],
                vuelo['fecha'],
                vuelo['codigo_aerolinea'],
                vuelo['nombre_aerolinea'],
                vuelo['aeropuerto_origen'],
                vuelo['aeropuerto_destino'],
                f"{vuelo['retraso_min']:+.2f}"
            ])
        
        print(tabulate(tabla_ultimos, headers=headers, tablefmt="grid"))
    
    print("\n" + "="*100 + "\n")
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("\n" + "="*100)
    print(" "*25 + "REQUERIMIENTO 2: VUELOS CON ANTICIPO EN LLEGADA")
    print("="*100)
    
    # Solicitar datos de entrada
    dest = input("\nIngrese el código del aeropuerto de destino (ej: JFK): ").strip().upper()
    
    try:
        min_anticipation = float(input("Ingrese el anticipo mínimo en minutos: "))
        max_anticipation = float(input("Ingrese el anticipo máximo en minutos: "))
    except ValueError:
        print("Error: Debe ingresar valores numéricos válidos.")
        return
    
    if min_anticipation > max_anticipation:
        print("Error: El anticipo mínimo no puede ser mayor que el máximo.")
        return
    
    if min_anticipation < 0 or max_anticipation < 0:
        print("Error: Los valores de anticipo deben ser positivos.")
        return
    
    # Ejecutar requerimiento
    tiempo, total, primeros, ultimos = l.req_2(control, dest, min_anticipation, max_anticipation)
    
    # Mostrar resultados
    print("\n" + "-"*100)
    print("RESULTADOS")
    print("-"*100)
    print(f"Tiempo de ejecución: {tiempo:.2f} ms")
    print(f"Total de vuelos encontrados: {total:,}")
    print(f"Aeropuerto de destino: {dest}")
    print(f"Rango de anticipo: [{min_anticipation}, {max_anticipation}] minutos")
    
    if total == 0:
        print("\nNo se encontraron vuelos que cumplan con los criterios especificados.")
        print("="*100 + "\n")
        return
    
    # Mostrar primeros 5 vuelos
    if al.size(primeros) > 0:
        print("\n" + "-"*100)
        if total <= 10:
            print(" "*35 + f"TODOS LOS VUELOS ({total})")
        else:
            print(" "*35 + "PRIMEROS 5 VUELOS")
        print("-"*100)
        
        tabla_primeros = []
        for i in range(al.size(primeros)):
            vuelo = al.get_element(primeros, i)
            tabla_primeros.append([
                vuelo['id'],
                vuelo['flight'],
                vuelo['date'],
                vuelo['airline_code'],
                vuelo['airline_name'],
                vuelo['origin'],
                vuelo['dest'],
                f"{vuelo['anticipation_min']:.2f}"
            ])
        
        headers = ["ID", "Código\nVuelo", "Fecha", "Cód.\nAerolínea", "Nombre Aerolínea", 
                   "Origen", "Destino", "Anticipo\n(min)"]
        print(tabulate(tabla_primeros, headers=headers, tablefmt="grid"))
    
    # Mostrar últimos 5 vuelos si hay más de 10
    if al.size(ultimos) > 0 and total > 10:
        print("\n" + "-"*100)
        print(" "*35 + "ÚLTIMOS 5 VUELOS")
        print("-"*100)
        
        tabla_ultimos = []
        for i in range(al.size(ultimos)):
            vuelo = al.get_element(ultimos, i)
            tabla_ultimos.append([
                vuelo['id'],
                vuelo['flight'],
                vuelo['date'],
                vuelo['airline_code'],
                vuelo['airline_name'],
                vuelo['origin'],
                vuelo['dest'],
                f"{vuelo['anticipation_min']:.2f}"
            ])
        
        print(tabulate(tabla_ultimos, headers=headers, tablefmt="grid"))
    
    print("\n" + "="*100 + "\n")
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
