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
                f"{vuelo['retraso_min']:+.2f}" 
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

    tiempo, total, primeros, ultimos = l.req_2(control, dest, min_anticipation, max_anticipation)

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
    print("\n" + "="*100)
    print(" "*20 + "REQUERIMIENTO 3: VUELOS POR AEROLÍNEA, DESTINO Y DISTANCIA")
    print("="*100)
    
    # Solicitar datos de entrada
    c_carrier = input("\nIngrese el código de la aerolínea (ej: AA, EV, UA): ").strip().upper()
    
    print("\nEjemplos de aeropuertos: JFK, LAX, DEN, BOS, SFO, EWR, LGA, PHX, FLL, MCO")
    c_destino = input("Ingrese el código del aeropuerto de destino: ").strip().upper()
    
    print("\nIngrese el rango de distancias (en millas):")
    try:
        d_min = float(input("  Distancia mínima: "))
        d_max = float(input("  Distancia máxima: "))
    except ValueError:
        print("Error: Las distancias deben ser valores numéricos.")
        return

    if d_min > d_max:
        print("Error: La distancia mínima no puede ser mayor que la máxima.")
        return
    
    if d_min < 0 or d_max < 0:
        print("Error: Las distancias deben ser valores positivos.")
        return

    rango_d = [d_min, d_max]
    tiempo, total, primeros, ultimos = l.req_3(control, c_carrier, c_destino, rango_d)

    print("\n" + "-"*100)
    print("RESULTADOS")
    print("-"*100)
    print(f"Tiempo de ejecución: {tiempo:.2f} ms")
    print(f"Total de vuelos encontrados: {total:,}")
    print(f"Aerolínea: {c_carrier}")
    print(f"Destino: {c_destino}")
    print(f"Rango de distancias: {d_min} - {d_max} millas")
    
    if total == 0:
        print("\nNo se encontraron vuelos que cumplan con los criterios especificados.")
        print("="*100 + "\n")
        return

    if al.size(primeros) > 0:
        print("\n" + "-"*100)
        if total <= 10:
            print(" "*35 + f"TODOS LOS VUELOS ({total})")
        else:
            print(" "*40 + "PRIMEROS 5 VUELOS")
        print("-"*100)
        
        tabla_primeros = []
        for i in range(al.size(primeros)):
            vuelo = al.get_element(primeros, i)
            tabla_primeros.append([
                vuelo['id'],
                vuelo['flight'],
                vuelo['date'],
                vuelo["Hora_llegada_real"],
                vuelo['carrier'],
                vuelo['name'],
                vuelo['origin'],
                vuelo['dest'],
                f"{vuelo['distance']:.2f}"
            ])
        
        headers = ["ID", "Código\nVuelo", "Fecha", "Hora", "Cód.\nAerolínea", 
                   "Nombre Aerolínea", "Origen", "Destino", "Distancia\n(millas)"]
        print(tabulate(tabla_primeros, headers=headers, tablefmt="grid"))

    if al.size(ultimos) > 0 and total > 10:
        print("\n" + "-"*100)
        print(" "*40 + "ÚLTIMOS 5 VUELOS")
        print("-"*100)
        
        tabla_ultimos = []
        for i in range(al.size(ultimos)):
            vuelo = al.get_element(ultimos, i)
            tabla_ultimos.append([
                vuelo['id'],
                vuelo['flight'],
                vuelo['date'],
                vuelo["Hora_llegada_real"],
                vuelo['carrier'],
                vuelo['name'],
                vuelo['origin'],
                vuelo['dest'],
                f"{vuelo['distance']:.2f}"
            ])
        
        print(tabulate(tabla_ultimos, headers=headers, tablefmt="grid"))
    
    print("\n" + "="*100 + "\n")
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    print("\n" + "="*120)
    print(" "*25 + "REQUERIMIENTO 4: AEROLÍNEAS CON MÁS VUELOS EN FRANJA HORARIA")
    print("="*120)

    print("\nIngrese el rango de fechas (formato AAAA-MM-DD):")
    f_inicial = input("  Fecha inicial: ").strip()
    f_final = input("  Fecha final: ").strip()
    
    print("\nIngrese la franja horaria de salida (formato HH:MM):")
    h_inicio = input("  Hora inicio: ").strip()
    h_final = input("  Hora final: ").strip()
    
    try:
        n = int(input("\nIngrese la cantidad N de aerolíneas a mostrar: "))
    except ValueError:
        print("Error: N debe ser un número entero.")
        return

    tiempo, total, aerolineas = l.req_4(control, f_inicial, f_final, h_inicio, h_final, n)
 
    print("\n" + "-"*120)
    print("RESULTADOS")
    print("-"*120)
    print(f"Tiempo de ejecución: {tiempo:.2f} ms")
    print(f"Total de aerolíneas consideradas: {total}")
    print(f"Rango de fechas: {f_inicial} a {f_final}")
    print(f"Franja horaria: {h_inicio} - {h_final}")
    print(f"Top {n} aerolíneas con más vuelos")
    
    if total == 0:
        print("\nNo se encontraron aerolíneas que cumplan con los criterios especificados.")
        print("="*120 + "\n")
        return

    print("\n" + "-"*120)
    print(" "*35 + f"TOP {total} AEROLÍNEAS POR CANTIDAD DE VUELOS")
    print("-"*120)
    
    tabla = []
    for i in range(al.size(aerolineas)):
        aerolinea = al.get_element(aerolineas, i)
        tabla.append([
            i + 1,
            aerolinea['codigo_aerolinea'],
            aerolinea['nombre_aerolinea'],
            f"{aerolinea['vuelos_programados']:,}",
            f"{aerolinea['duracion_promedio_min']:.2f}",
            f"{aerolinea['distancia_promedio_millas']:.2f}"
        ])
    
    headers = ["#", "Código", "Nombre Aerolínea", "Vuelos\nProgramados", 
               "Duración\nPromedio (min)", "Distancia\nPromedio (mi)"]
    print(tabulate(tabla, headers=headers, tablefmt="grid"))
    
    print("\n" + "-"*120)
    print(" "*35 + "VUELO DE MENOR DURACIÓN POR AEROLÍNEA")
    print("-"*120)
    
    for i in range(al.size(aerolineas)):
        aerolinea = al.get_element(aerolineas, i)
        vuelo = aerolinea['vuelo_menor_duracion']
        
        print(f"\n{i+1}. {aerolinea['nombre_aerolinea']} ({aerolinea['codigo_aerolinea']})")
        print(f"      • Vuelo con menor duracion:")
        print(f"      • ID: {vuelo['id']}")
        print(f"      • Código: {vuelo['codigo_vuelo']}")
        print(f"      • Salida programada: {vuelo['fecha_hora_salida_programada']}")
        print(f"      • Ruta: {vuelo['origen']} → {vuelo['destino']}")
        print(f"      • Duración: {vuelo['duracion_min']:.2f} min")
    
    print("\n" + "="*120 + "\n")
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    print("\n" + "="*120)
    print(" "*25 + "REQUERIMIENTO 5: AEROLÍNEAS MÁS PUNTUALES EN LLEGADA")
    print("="*120)
    
    # Solicitar datos de entrada
    print("\nIngrese el rango de fechas (formato AAAA-MM-DD):")
    f_inicial = input("  Fecha inicial: ").strip()
    f_final = input("  Fecha final: ").strip()
    
    print("\nEjemplos de aeropuertos: JFK, LAX, DEN, BOS, SFO, EWR, LGA, PHX, FLL, MCO")
    destino = input("Ingrese el código del aeropuerto de destino: ").strip().upper()
    
    try:
        n = int(input("\nIngrese la cantidad N de aerolíneas a mostrar: "))
    except ValueError:
        print("Error: N debe ser un número entero.")
        return
    

    tiempo, total, aerolineas = l.req_5(control, f_inicial, f_final, destino, n)

    print("\n" + "-"*120)
    print("RESULTADOS")
    print("-"*120)
    print(f"Tiempo de ejecución: {tiempo:.2f} ms")
    print(f"Total de aerolíneas consideradas: {total}")
    print(f"Rango de fechas: {f_inicial} a {f_final}")
    print(f"Aeropuerto de destino: {destino}")
    print(f"Top {n} aerolíneas más puntuales")
    
    if total == 0:
        print("\nNo se encontraron aerolíneas que cumplan con los criterios especificados.")
        print("Verifique que el código del aeropuerto sea correcto y que existan vuelos en ese rango de fechas.")
        print("="*120 + "\n")
        return
    
    # Mostrar tabla de aerolíneas
    print("\n" + "-"*120)
    print(" "*35 + f"TOP {total} AEROLÍNEAS MÁS PUNTUALES")
    print("-"*120)
    
    tabla = []
    for i in range(al.size(aerolineas)):
        aerolinea = al.get_element(aerolineas, i)
        tabla.append([
            i + 1,
            aerolinea['codigo_aerolinea'],
            aerolinea['nombre_aerolinea'],
            f"{aerolinea['vuelos_analizados']:,}",
            f"{aerolinea['puntualidad_promedio_min']:+.2f}",
            f"{aerolinea['duracion_promedio_min']:.2f}",
            f"{aerolinea['distancia_promedio_millas']:.2f}"
        ])
    
    headers = ["#", "Código", "Nombre Aerolínea", "Vuelos\nAnalizados", 
               "Puntualidad\nPromedio (min)", "Duración\nPromedio (min)", "Distancia\nPromedio (mi)"]
    print(tabulate(tabla, headers=headers, tablefmt="grid"))
    
    # Mostrar detalles de vuelo de mayor distancia
    print("\n" + "-"*120)
    print(" "*35 + "VUELO DE MAYOR DISTANCIA POR AEROLÍNEA")
    print("-"*120)
    
    for i in range(al.size(aerolineas)):
        aerolinea = al.get_element(aerolineas, i)
        vuelo = aerolinea['vuelo_mayor_distancia']
        
        print(f"\n {i+1}. {aerolinea['nombre_aerolinea']} ({aerolinea['codigo_aerolinea']})")
        print(f"      • Vuelo de mayor distancia recorrida:")
        print(f"      • ID: {vuelo['id']}")
        print(f"      • Código: {vuelo['codigo_vuelo']}")
        print(f"      • Llegada: {vuelo['fecha_hora_llegada']}")
        print(f"      • Ruta: {vuelo['origen']} → {vuelo['destino']}")
        print(f"      • Duración: {vuelo['duracion_min']:.2f} min")
    
    print("\n" + "="*120)
    print("Nota: Puntualidad cercana a 0 = Más puntual | Positivo = Retraso | Negativo = Anticipo")
    print("="*120 + "\n")
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    print("\n" + "="*120)
    print(" "*30 + "REQUERIMIENTO 6: AEROLÍNEAS MÁS ESTABLES EN HORA DE SALIDA")
    print("="*120)

    print("\nIngrese el rango de fechas (formato AAAA-MM-DD):")
    f_inicial = input("  Fecha inicial: ").strip()
    f_final = input("  Fecha final: ").strip()
    
    print("\nIngrese el rango de distancias (en millas):")
    try:
        d_min = float(input("  Distancia mínima: "))
        d_max = float(input("  Distancia máxima: "))
    except ValueError:
        print("Error: Las distancias deben ser valores numéricos.")
        return
    
    try:
        m = int(input("\nIngrese la cantidad M de aerolíneas a mostrar: "))
    except ValueError:
        print("Error: M debe ser un número entero.")
        return

    tiempo, total, aerolineas = l.req_6(control, f_inicial, f_final, d_min, d_max, m)

    print("\n" + "-"*120)
    print("RESULTADOS")
    print("-"*120)
    print(f"Tiempo de ejecución: {tiempo:.2f} ms")
    print(f"Total de aerolíneas analizadas: {total}")
    print(f"Rango de fechas: {f_inicial} a {f_final}")
    print(f"Rango de distancias: {d_min} - {d_max} millas")
    print(f"Top {m} aerolíneas más estables")
    
    if total == 0:
        print("\nNo se encontraron aerolíneas que cumplan con los criterios especificados.")
        print("="*120 + "\n")
        return

    print("\n" + "-"*120)
    print(" "*40 + f"TOP {total} AEROLÍNEAS MÁS ESTABLES")
    print("-"*120)
    
    tabla = []
    for i in range(al.size(aerolineas)):
        aerolinea = al.get_element(aerolineas, i)
        tabla.append([
            i + 1,
            aerolinea['codigo_aerolinea'],
            aerolinea['nombre_aerolinea'],
            f"{aerolinea['vuelos_analizados']:,}",
            f"{aerolinea['promedio_min']:+.2f}",
            f"{aerolinea['estabilidad_min']:.2f}"
        ])
    
    headers = ["#", "Código", "Nombre Aerolínea", "Vuelos\nAnalizados", 
               "Promedio\nRetraso (min)", "Estabilidad\n(Desv. Est. (min))"]
    print(tabulate(tabla, headers=headers, tablefmt="grid"))

    print("\n" + "-"*120)
    print(" "*35 + "DETALLE DE VUELO MÁS CERCANO AL PROMEDIO")
    print("-"*120)
    
    for i in range(al.size(aerolineas)):
        aerolinea = al.get_element(aerolineas, i)
        vuelo = aerolinea['vuelo_cercano']
        
        print(f"\n {i+1}. {aerolinea['nombre_aerolinea']} ({aerolinea['codigo_aerolinea']})")
        print(f"• Vuelo con retraso mas cercano al promedio:")
        print(f"• ID: {vuelo['id']}")
        print(f"• Código: {vuelo['codigo_vuelo']}")
        print(f"• Salida: {vuelo['fecha_hora_salida']}")
        print(f"• Ruta: {vuelo['origen']} → {vuelo['destino']}")
    
    print("\n" + "="*120)
    print("Nota: Menor desviación estándar = Mayor estabilidad en horarios de salida")
    print("="*120 + "\n")
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

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
