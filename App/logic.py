import time
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.priority_queue import priority_queue as pq
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.Tree import red_black_tree as rbt
from datetime import datetime
import csv
from math import sqrt


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

    for vuelo in archivo:
        vuelo["flight_date"] = datetime.strptime(vuelo["flight_date"], "%Y-%m-%d")

        hora_salida = vuelo["departure_time"] if vuelo["departure_time"] != "" else "00:00"
        hora_llegada = vuelo["arrival_time"] if vuelo["arrival_time"] != "" else "00:00"
        vuelo["departure_time"] = datetime.strptime(hora_salida, "%H:%M").time()
        vuelo["arrival_time"] = datetime.strptime(hora_llegada, "%H:%M").time()

        vuelo["air_time"] = float(vuelo["air_time"]) if vuelo["air_time"] != "" else 0.0
        vuelo["distance"] = float(vuelo["distance"]) if vuelo["distance"] != "" else 0.0

        al.add_last(catalog["flights"], vuelo)

    tamanio = catalog["flights"]["size"]

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

    final = get_time()
    tiempo = delta_time(inicio, final)
    retorno = catalog, tiempo, tamanio, primeros, ultimos
    return retorno

def req_1(catalog, code, min_delay, max_delay):
        
    inicio = get_time()

    vuelos = catalog["flights"]
    filtrados = al.new_list()

    for i in range(al.size(vuelos)):
        v = al.get_element(vuelos, i)

        if v["carrier"] == code:
            sched = v["sched_dep_time"]
            real = v["dep_time"]

            if sched == "" or real == "":
                continue

            sched_h = datetime.strptime(sched, "%H:%M")
            real_h = datetime.strptime(real, "%H:%M")

            diff = (real_h - sched_h).total_seconds() / 60

            # Ajuste si cruza la medianoche
            if diff < -720:
                diff += 1440
            elif diff > 720:
                diff -= 1440

            if min_delay <= diff <= max_delay:
                v["retraso"] = round(diff, 2)
                al.add_last(filtrados, v)

    arbol = bst.new_map()

    for i in range(al.size(filtrados)):
        vuelo = al.get_element(filtrados, i)
        # clave: tupla (retraso, fecha, hora)
        key = (vuelo["retraso"], vuelo["date"], vuelo["dep_time"])
        bst.put(arbol, key, vuelo)

    def inorder_rec(nodo, lista):
        if nodo is not None:
            inorder_rec(nodo["left"], lista)
            al.add_last(lista, nodo["value"])
            inorder_rec(nodo["right"], lista)

    def inorder(tree):
        lista = al.new_list()
        inorder_rec(tree["root"], lista)
        return lista

    filtrados = inorder(arbol)

    total = al.size(filtrados)
    primeros = al.new_list()
    ultimos = al.new_list()
    limite = min(5, total)

    for i in range(limite):
        elem = al.get_element(filtrados, i)
        info = {
            "id_vuelo": elem["id"],
            "codigo_vuelo": elem["flight"],
            "fecha": elem["date"],
            "nombre_aerolinea": elem["name"],
            "codigo_aerolinea": elem["carrier"],
            "aeropuerto_origen": elem["origin"],
            "aeropuerto_destino": elem["dest"],
            "retraso_min": round(elem["retraso"], 2)
        }
        al.add_last(primeros, info)

    for i in range(total - limite, total):
        elem = al.get_element(filtrados, i)
        info = {
            "id_vuelo": elem["id"],
            "codigo_vuelo": elem["flight"],
            "fecha": elem["date"],
            "nombre_aerolinea": elem["name"],
            "codigo_aerolinea": elem["carrier"],
            "aeropuerto_origen": elem["origin"],
            "aeropuerto_destino": elem["dest"],
            "retraso_min": round(elem["retraso"], 2)
        }
        al.add_last(ultimos, info)

    final = get_time()
    tiempo = delta_time(inicio, final)

    resultado = al.new_list()
    al.add_last(resultado, {"tiempo_ms": round(tiempo, 2)})
    al.add_last(resultado, {"total_vuelos": total})
    al.add_last(resultado, {"primeros": primeros})
    al.add_last(resultado, {"ultimos": ultimos})

    return resultado

def req_2(catalog, dest, min_anticipation, max_anticipation):

    inicio = get_time()

    flights = catalog["flights"]
    filtrados = al.new_list()

    for i in range(al.size(flights)):
        vuelo = al.get_element(flights, i)

        if vuelo["dest"] == dest:
            sched_arr = vuelo["sched_arr_time"]
            real_arr = vuelo["arr_time"]

            if sched_arr == "" or real_arr == "":
                continue

            sched_time = datetime.strptime(sched_arr, "%H:%M")
            real_time = datetime.strptime(real_arr, "%H:%M")

            diff = (real_time - sched_time).total_seconds() / 60

            if diff < -720:
                diff += 1440
            elif diff > 720:
                diff -= 1440

            if diff < 0:
                anticipo = abs(diff)
                if min_anticipation <= anticipo <= max_anticipation:
                    vuelo["anticipation"] = round(anticipo, 2)
                    al.add_last(filtrados, vuelo)

    arbol = bst.new_map()

    for i in range(al.size(filtrados)):
        vuelo = al.get_element(filtrados, i)
        key = (vuelo["anticipation"], vuelo["date"], vuelo["arr_time"])
        bst.put(arbol, key, vuelo)

    def inorder_rec(nodo, lista):
        if nodo is not None:
            inorder_rec(nodo["left"], lista)
            al.add_last(lista, nodo["value"])
            inorder_rec(nodo["right"], lista)

    def inorder(arbol):
        lista = al.new_list()
        inorder_rec(arbol["root"], lista)
        return lista

    filtrados = inorder(arbol)

    total = al.size(filtrados)
    primeros = al.new_list()
    ultimos = al.new_list()
    limite = min(5, total)

    for i in range(limite):
        f = al.get_element(filtrados, i)
        info = {
            "id": f["id"],
            "flight": f["flight"],
            "date": f["date"],
            "airline_name": f["name"],
            "airline_code": f["carrier"],
            "origin": f["origin"],
            "dest": f["dest"],
            "anticipation_min": f["anticipation"]
        }
        al.add_last(primeros, info)

    for i in range(total - limite, total):
        f = al.get_element(filtrados, i)
        info = {
            "id": f["id"],
            "flight": f["flight"],
            "date": f["date"],
            "airline_name": f["name"],
            "airline_code": f["carrier"],
            "origin": f["origin"],
            "dest": f["dest"],
            "anticipation_min": f["anticipation"]
        }
        al.add_last(ultimos, info)

    final = get_time()
    tiempo = delta_time(inicio, final)
    retorno = al.new_list()

    al.add_last(retorno, {"tiempo": round(tiempo, 2)})
    al.add_last(retorno, {"total_vuelos": total})
    al.add_last(retorno, {"primeros": primeros})
    al.add_last(retorno, {"ultimos": ultimos})

    return retorno

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

def req_6(catalog,f_inicial, f_final, d_min, d_max, m):
       
    inicio = get_time()
    flights = catalog["flights"]

    por_aerolinea = mlp.new_map(al.size(flights), 0.7)

    fecha_ini = datetime.strptime(f_inicial, "%Y-%m-%d")
    fecha_fin = datetime.strptime(f_final, "%Y-%m-%d")

    for i in range(al.size(flights)):
        v = al.get_element(flights, i)

        if v["date"] != "" and v["distance"] != "":
            f_v = datetime.strptime(v["date"], "%Y-%m-%d")
            dist = float(v["distance"])

            if (fecha_ini <= f_v <= fecha_fin) and (d_min <= dist <= d_max):
                sched_dep = v["sched_dep_time"]
                real_dep = v["dep_time"]

                if sched_dep != "" and real_dep != "":
                    t_sched = datetime.strptime(sched_dep, "%H:%M")
                    t_real = datetime.strptime(real_dep, "%H:%M")
                    diff = (t_real - t_sched).total_seconds() / 60.0

                    # Ajuste por cruce de medianoche
                    if diff < -720:
                        diff += 1440
                    elif diff > 720:
                        diff -= 1440

                    code = v["carrier"]
                    reg = mlp.get(por_aerolinea, code)
                    if reg is None:
                        reg = {
                            "code": code,
                            "name": v["name"],
                            "delays": al.new_list(),
                            "flights": al.new_list()
                        }

                    al.add_last(reg["delays"], diff)

                    info_vuelo = {
                        "id": v["id"],
                        "flight": v["flight"],
                        "date": v["date"],
                        "dep_time": v["dep_time"],
                        "origin": v["origin"],
                        "dest": v["dest"],
                        "delay": diff
                    }

                    al.add_last(reg["flights"], info_vuelo)
                    mlp.put(por_aerolinea, code, reg)

    def promedio(lista):
        n = al.size(lista)
        if n == 0:
            return 0.0
        suma = 0.0
        for i in range(n):
            suma += float(al.get_element(lista, i))
        return suma / n

    def desviacion(lista, mu):
        n = al.size(lista)
        if n <= 1:
            return 0.0
        suma2 = 0.0
        for i in range(n):
            x = float(al.get_element(lista, i))
            d = x - mu
            suma2 += d * d
        return sqrt(suma2 / n)

    def vuelo_mas_cercano(prom, vuelos):
        mejor = None
        mejor_abs = None
        for i in range(al.size(vuelos)):
            fv = al.get_element(vuelos, i)
            d = abs(fv["delay"] - prom)
            if (mejor is None) or (d < mejor_abs):
                mejor = fv
                mejor_abs = d
        return mejor
    
    heap = pq.new_heap(is_min_pq=True)
    keys = mlp.key_set(por_aerolinea)

    for i in range(al.size(keys)):
        k = al.get_element(keys, i)
        reg = mlp.get(por_aerolinea, k)
        n_vuelos = al.size(reg["delays"])

        if n_vuelos > 0:
            mu = promedio(reg["delays"])
            sd = desviacion(reg["delays"], mu)
            cercano = vuelo_mas_cercano(mu, reg["flights"])

            resumen = {
                "codigo_aerolinea": reg["code"],
                "vuelos_analizados": n_vuelos,
                "promedio_min": round(mu, 2),
                "estabilidad_min": round(sd, 2),
                "vuelo_cercano": {
                    "id": cercano["id"],
                    "codigo_vuelo": cercano["flight"],
                    "fecha_hora_salida": f'{cercano["date"]} {cercano["dep_time"]}',
                    "origen": cercano["origin"],
                    "destino": cercano["dest"]
                }
            }

            pq.insert(heap, (sd, mu), resumen)

    aerolineas = al.new_list()
    total_heap = pq.size(heap)
    extraer = m
    if total_heap < m:
        extraer = total_heap

    j = 0
    while j < extraer:
        val = pq.remove(heap)
        al.add_last(aerolineas, val)
        j += 1

    final = get_time()
    tiempo = delta_time(inicio, final)

    retorno = al.new_list()
    al.add_last(retorno, {"tiempo": round(tiempo, 2)})
    al.add_last(retorno, {"total_aerolineas": extraer})
    al.add_last(retorno, {"aerolineas": aerolineas})

    return retorno


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
