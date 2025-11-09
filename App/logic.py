import time
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.priority_queue import priority_queue as pq
from datetime import datetime
import csv


def new_logic():
    catalog = {
        "flights": al.new_list(),
    }
    return catalog


# Funciones para la carga de datos

def load_data(catalog, filename):
    inicio = get_time()

    n_archivo = "Data/" + filename
    archivo = csv.DictReader(open(n_archivo, encoding='utf-8'))

    # ------------------------------
    # Lectura y conversión de datos
    # ------------------------------
    for vuelo in archivo:
        vuelo["flight_date"] = datetime.strptime(vuelo["flight_date"], "%Y-%m-%d")

        # Si los campos de hora están vacíos, se reemplazan por "00:00"
        hora_salida = vuelo["departure_time"] if vuelo["departure_time"] != "" else "00:00"
        hora_llegada = vuelo["arrival_time"] if vuelo["arrival_time"] != "" else "00:00"
        vuelo["departure_time"] = datetime.strptime(hora_salida, "%H:%M").time()
        vuelo["arrival_time"] = datetime.strptime(hora_llegada, "%H:%M").time()

        # Conversión a float
        vuelo["air_time"] = float(vuelo["air_time"]) if vuelo["air_time"] != "" else 0.0
        vuelo["distance"] = float(vuelo["distance"]) if vuelo["distance"] != "" else 0.0

        al.add_last(catalog["flights"], vuelo)

    tamanio = catalog["flights"]["size"]

    # ------------------------------
    # Ordenar por fecha y hora
    # ------------------------------
    vuelos_ordenados = al.new_list()
    for i in range(0, tamanio):
        elem = al.get_element(catalog["flights"], i)
        al.add_last(vuelos_ordenados, elem)

    def sort_crit(v1, v2):
        """Criterio de ordenamiento: fecha + hora de salida"""
        fecha1 = v1["flight_date"]
        fecha2 = v2["flight_date"]
        hora1 = v1["departure_time"]
        hora2 = v2["departure_time"]
        if fecha1 < fecha2:
            return True
        elif fecha1 == fecha2 and hora1 < hora2:
            return True
        return False

    vuelos_ordenados = al.merge_sort(vuelos_ordenados, sort_crit)

    # ------------------------------
    # Primeros y últimos 5 vuelos
    # ------------------------------
    primeros = []
    ultimos = []
    fmt_fecha = "%Y-%m-%d"
    fmt_hora = "%H:%M"

    for i in range(0, 5):
        vuelo = al.get_element(vuelos_ordenados, i)
        info = {
            "fecha": vuelo["flight_date"].strftime(fmt_fecha),
            "hora_salida": vuelo["departure_time"].strftime(fmt_hora),
            "hora_llegada": vuelo["arrival_time"].strftime(fmt_hora),
            "codigo_aerolinea": vuelo["airline_iata"],
            "nombre_aerolinea": vuelo["airline_name"],
            "aeronave": vuelo["tail_number"],
            "origen": vuelo["origin_airport"],
            "destino": vuelo["destination_airport"],
            "duracion_min": round(vuelo["air_time"], 2),
            "distancia_millas": round(vuelo["distance"], 2)
        }
        primeros.append(info)

    for i in range(tamanio - 5, tamanio):
        vuelo = al.get_element(vuelos_ordenados, i)
        info = {
            "fecha": vuelo["flight_date"].strftime(fmt_fecha),
            "hora_salida": vuelo["departure_time"].strftime(fmt_hora),
            "hora_llegada": vuelo["arrival_time"].strftime(fmt_hora),
            "codigo_aerolinea": vuelo["airline_iata"],
            "nombre_aerolinea": vuelo["airline_name"],
            "aeronave": vuelo["tail_number"],
            "origen": vuelo["origin_airport"],
            "destino": vuelo["destination_airport"],
            "duracion_min": round(vuelo["air_time"], 2),
            "distancia_millas": round(vuelo["distance"], 2)
        }
        ultimos.append(info)

    # ------------------------------
    # Tiempo total y retorno
    # ------------------------------
    final = get_time()
    tiempo = delta_time(inicio, final)

    retorno = catalog, tiempo, tamanio, primeros, ultimos
    return retorno

def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
