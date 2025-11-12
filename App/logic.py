import time
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.priority_queue import priority_queue as pq
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.List import list_node as n
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
        # Procesar fecha
        vuelo["date"] = datetime.strptime(vuelo["date"], "%Y-%m-%d")

        # Procesar horas de salida y llegada REALES (dep_time y arr_time)
        hora_salida = vuelo["dep_time"] if vuelo["dep_time"] != "" else "00:00"
        hora_llegada = vuelo["arr_time"] if vuelo["arr_time"] != "" else "00:00"
        vuelo["dep_time"] = datetime.strptime(hora_salida, "%H:%M").time()
        vuelo["arr_time"] = datetime.strptime(hora_llegada, "%H:%M").time()
        
        # Procesar horas programadas (para ordenar)
        hora_salida_prog = vuelo["sched_dep_time"] if vuelo["sched_dep_time"] != "" else "00:00"
        vuelo["sched_dep_time"] = datetime.strptime(hora_salida_prog, "%H:%M").time()
        
        hora_llegada_prog = vuelo["sched_arr_time"] if vuelo["sched_arr_time"] != "" else "00:00"
        vuelo["sched_arr_time"] = datetime.strptime(hora_llegada_prog, "%H:%M").time()

        # Procesar campos numéricos
        vuelo["air_time"] = float(vuelo["air_time"]) if vuelo["air_time"] != "" else 0.0
        vuelo["distance"] = float(vuelo["distance"]) if vuelo["distance"] != "" else 0.0

        al.add_last(catalog["flights"], vuelo)

    tamanio = catalog["flights"]["size"]

    # Copiar lista para ordenar
    vuelos_ordenados = al.new_list()
    for i in range(0, tamanio):
        elem = al.get_element(catalog["flights"], i)
        al.add_last(vuelos_ordenados, elem)

    def sort_crit(v1, v2):
        """Criterio de ordenamiento: fecha + hora programada de salida"""
        fecha1 = v1["date"]
        fecha2 = v2["date"]
        hora1 = v1["sched_dep_time"]
        hora2 = v2["sched_dep_time"]
        if fecha1 < fecha2:
            return True
        elif fecha1 == fecha2 and hora1 < hora2:
            return True
        return False

    vuelos_ordenados = al.merge_sort(vuelos_ordenados, sort_crit)

    # Extraer primeros 5 vuelos
    primeros = []
    ultimos = []
    fmt_fecha = "%Y-%m-%d"
    fmt_hora = "%H:%M"

    for i in range(0, min(5, tamanio)):
        vuelo = al.get_element(vuelos_ordenados, i)
        info = {
            "fecha": vuelo["date"].strftime(fmt_fecha),
            "hora_salida": vuelo["dep_time"].strftime(fmt_hora),
            "hora_llegada": vuelo["arr_time"].strftime(fmt_hora),
            "codigo_aerolinea": vuelo["carrier"],
            "nombre_aerolinea": vuelo["name"],
            "aeronave": vuelo["tailnum"],
            "origen": vuelo["origin"],
            "destino": vuelo["dest"],
            "duracion_min": round(vuelo["air_time"], 2),
            "distancia_millas": round(vuelo["distance"], 2)
        }
        primeros.append(info)

    # Extraer últimos 5 vuelos
    for i in range(max(0, tamanio - 5), tamanio):
        vuelo = al.get_element(vuelos_ordenados, i)
        info = {
            "fecha": vuelo["date"].strftime(fmt_fecha),
            "hora_salida": vuelo["dep_time"].strftime(fmt_hora),
            "hora_llegada": vuelo["arr_time"].strftime(fmt_hora),
            "codigo_aerolinea": vuelo["carrier"],
            "nombre_aerolinea": vuelo["name"],
            "aeronave": vuelo["tailnum"],
            "origen": vuelo["origin"],
            "destino": vuelo["dest"],
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


            sched_min = sched.hour * 60 + sched.minute
            real_min = real.hour * 60 + real.minute

            diff = real_min - sched_min

            # Ajuste si cruza la medianoche
            if diff < -720:  
                diff += 1440
            elif diff > 720:  
                diff -= 1440

            if min_delay <= diff <= max_delay:
                vuelo_con_retraso = v.copy()
                vuelo_con_retraso["retraso"] = round(diff, 2)
                al.add_last(filtrados, vuelo_con_retraso)

    arbol = bst.new_map()

    for i in range(al.size(filtrados)):
        vuelo = al.get_element(filtrados, i)
        key = (vuelo["retraso"], vuelo["date"], vuelo["dep_time"])
        bst.put(arbol, key, vuelo)

    def inorder_rec(nodo, lista):
        if nodo is not None:
            inorder_rec(nodo["left"], lista)
            al.add_last(lista, nodo["value"])
            inorder_rec(nodo["right"], lista)

    def inorder(tree):
        lista = al.new_list()
        if tree["root"] is not None:
            inorder_rec(tree["root"], lista)
        return lista

    filtrados_ordenados = inorder(arbol)
    total = al.size(filtrados_ordenados)

    primeros = al.new_list()
    ultimos = al.new_list()
    limite = min(5, total)

    for i in range(limite):
        elem = al.get_element(filtrados_ordenados, i)
        info = {
            "id_vuelo": elem["id"],
            "codigo_vuelo": elem["flight"],
            "fecha": elem["date"].strftime("%Y-%m-%d"),
            "nombre_aerolinea": elem["name"],
            "codigo_aerolinea": elem["carrier"],
            "aeropuerto_origen": elem["origin"],
            "aeropuerto_destino": elem["dest"],
            "retraso_min": elem["retraso"]
        }
        al.add_last(primeros, info)

    if total > 10:
        for i in range(total - 5, total):
            elem = al.get_element(filtrados_ordenados, i)
            info = {
                "id_vuelo": elem["id"],
                "codigo_vuelo": elem["flight"],
                "fecha": elem["date"].strftime("%Y-%m-%d"),
                "nombre_aerolinea": elem["name"],
                "codigo_aerolinea": elem["carrier"],
                "aeropuerto_origen": elem["origin"],
                "aeropuerto_destino": elem["dest"],
                "retraso_min": elem["retraso"]
            }
            al.add_last(ultimos, info)

    final = get_time()
    tiempo = delta_time(inicio, final)

    return tiempo, total, primeros, ultimos

def req_2(catalog, dest, min_anticipation, max_anticipation):

    inicio = get_time()

    flights = catalog["flights"]
    filtrados = al.new_list()

    for i in range(al.size(flights)):
        vuelo = al.get_element(flights, i)

        if vuelo["dest"] == dest:
            sched_arr = vuelo["sched_arr_time"]
            real_arr = vuelo["arr_time"]

            sched_min = sched_arr.hour * 60 + sched_arr.minute
            real_min = real_arr.hour * 60 + real_arr.minute

            diff = real_min - sched_min

            if diff < -720:
                diff += 1440
            elif diff > 720:
                diff -= 1440

            if diff < 0:
                anticipo = abs(diff)
                if min_anticipation <= anticipo <= max_anticipation:
                    vuelo_copia = dict(vuelo)
                    vuelo_copia["anticipation"] = round(anticipo, 2)
                    al.add_last(filtrados, vuelo_copia)

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

    def inorder(tree):
        lista = al.new_list()
        if tree["root"] is not None:
            inorder_rec(tree["root"], lista)
        return lista

    filtrados_ordenados = inorder(arbol)
    total = al.size(filtrados_ordenados)

    primeros = al.new_list()
    ultimos = al.new_list()
    limite = min(5, total)

    for i in range(limite):
        f = al.get_element(filtrados_ordenados, i)
        info = {
            "id": f["id"],
            "flight": f["flight"],
            "date": f["date"].strftime("%Y-%m-%d"),
            "airline_name": f["name"],
            "airline_code": f["carrier"],
            "origin": f["origin"],
            "dest": f["dest"],
            "anticipation_min": f["anticipation"]
        }
        al.add_last(primeros, info)

    if total > 10:
        for i in range(total - 5, total):
            f = al.get_element(filtrados_ordenados, i)
            info = {
                "id": f["id"],
                "flight": f["flight"],
                "date": f["date"].strftime("%Y-%m-%d"),
                "airline_name": f["name"],
                "airline_code": f["carrier"],
                "origin": f["origin"],
                "dest": f["dest"],
                "anticipation_min": f["anticipation"]
            }
            al.add_last(ultimos, info)

    final = get_time()
    tiempo = delta_time(inicio, final)

    return tiempo, total, primeros, ultimos

def req_3(catalog, c_carrier, c_destino, rango_d):
    """
    Retorna el resultado del requerimiento 3
    """
    # porsiacas rango_d es un list de dos elementos [min, max]

    inicio = get_time()

    rango_ini = rango_d[0]
    rango_fin = rango_d[1]
    vuelos = catalog["flights"]
    filtrados = al.new_list()
    
    for i in range(al.size(vuelos)):
        temp = al.get_element(vuelos, i)
        
        if temp["carrier"] == c_carrier and temp["dest"] == c_destino:
            # temp["distance"] ya es float
            distancia = temp["distance"]
            
            if rango_ini <= distancia <= rango_fin:
                al.add_last(filtrados, temp)
    
    # Usar RBT para ordenar por (distancia, fecha, hora_llegada_real)
    arbol = rbt.new_map()
    
    for i in range(al.size(filtrados)):
        vuelo = al.get_element(filtrados, i)
        key = (vuelo["distance"], vuelo["date"], vuelo["arr_time"])
        rbt.put(arbol, key, vuelo)
    
    # Recorrido inorder del RBT para obtener vuelos ordenados
    def inorder_rec(nodo, lista):
        if nodo is not None:
            inorder_rec(nodo["left"], lista)
            al.add_last(lista, nodo["value"])
            inorder_rec(nodo["right"], lista)

    def inorder(tree):
        lista = al.new_list()
        if tree["root"] is not None:
            inorder_rec(tree["root"], lista)
        return lista
    
    filtrados_ordenados = inorder(arbol)
    total = al.size(filtrados_ordenados)
    
    # Extraer primeros y últimos 5
    primeros = al.new_list()
    ultimos = al.new_list()
    
    if total > 10:
        # Primeros 5
        for i in range(5):
            vuelo = al.get_element(filtrados_ordenados, i)
            info = {
                "id": vuelo["id"],
                "flight": vuelo["flight"],
                "date": vuelo["date"].strftime("%Y-%m-%d"),
                "Hora_llegada_real": vuelo["arr_time"].strftime("%H:%M"),
                "carrier": vuelo["carrier"],
                "name": vuelo["name"],
                "origin": vuelo["origin"],
                "dest": vuelo["dest"],
                "distance": round(vuelo["distance"], 2)
            }
            al.add_last(primeros, info)
        
        # Últimos 5
        for i in range(total - 5, total):
            vuelo = al.get_element(filtrados_ordenados, i)
            info = {
                "id": vuelo["id"],
                "flight": vuelo["flight"],
                "date": vuelo["date"].strftime("%Y-%m-%d"),
                "Hora_llegada_real": vuelo["arr_time"].strftime("%H:%M"),
                "carrier": vuelo["carrier"],
                "name": vuelo["name"],
                "origin": vuelo["origin"],
                "dest": vuelo["dest"],
                "distance": round(vuelo["distance"], 2)
            }
            al.add_last(ultimos, info)
    else:
        # Si hay 10 o menos, mostrar todos en primeros
        for i in range(total):
            vuelo = al.get_element(filtrados_ordenados, i)
            info = {
                "id": vuelo["id"],
                "flight": vuelo["flight"],
                "date": vuelo["date"].strftime("%Y-%m-%d"),
                "Hora_llegada_real": vuelo["arr_time"].strftime("%H:%M"),
                "carrier": vuelo["carrier"],
                "name": vuelo["name"],
                "origin": vuelo["origin"],
                "dest": vuelo["dest"],
                "distance": round(vuelo["distance"], 2)
            }
            al.add_last(primeros, info)

    final = get_time()
    tiempo = delta_time(inicio, final)
    return tiempo, total, primeros, ultimos 


def req_4(catalog , f_inicial, f_final, h_inicio, h_final, n):

    inicio = get_time()
    flights = catalog["flights"]

    fecha_ini = datetime.strptime(f_inicial, "%Y-%m-%d")
    fecha_fin = datetime.strptime(f_final, "%Y-%m-%d")

    t_ini = datetime.strptime(h_inicio, "%H:%M").time()
    t_fin = datetime.strptime(h_final, "%H:%M").time()

    def en_franja(t):
        # Maneja franja normal y la que cruza medianoche
        if t_ini <= t_fin:
            return (t_ini <= t <= t_fin)
        else:
            # cruza medianoche: válido si t >= inicio o t <= final
            return (t >= t_ini) or (t <= t_fin)

    por_aerolinea = mlp.new_map(al.size(flights), 0.7)

    for i in range(al.size(flights)):
        v = al.get_element(flights, i)

        f_v = v["date"]
        if (fecha_ini <= f_v <= fecha_fin):
            t_prog = v["sched_dep_time"]
            if en_franja(t_prog):

                code = v["carrier"]
                reg = mlp.get(por_aerolinea, code)
                if reg is None:
                    reg = {
                        "code": code,
                        "name": v["name"],
                        "count": 0,
                        "sum_air": 0.0,
                        "sum_dist": 0.0,
                        "best_air": None,         # menor duración (float)
                        "best_dt_prog": None,     # datetime de fecha-hora programada (para desempate)
                        "best_flight": None       # dict con datos del vuelo ganador
                    }

                air = v["air_time"]
                dist = v["distance"]

                reg["count"] += 1
                reg["sum_air"] += air
                reg["sum_dist"] += dist

                # Candidato a vuelo de menor duración
                # Combinar fecha y hora para comparación cronológica
                dt_prog = datetime.combine(v["date"], v["sched_dep_time"])
                
                if (reg["best_air"] is None) or (air < reg["best_air"]) or \
                   (air == reg["best_air"] and dt_prog < reg["best_dt_prog"]):
                    reg["best_air"] = air
                    reg["best_dt_prog"] = dt_prog
                    reg["best_flight"] = {
                        "id": v["id"],
                        "flight": v["flight"],
                        "date": v["date"].strftime("%Y-%m-%d"),
                        "sched_dep_time": v["sched_dep_time"].strftime("%H:%M"),
                        "origin": v["origin"],
                        "dest": v["dest"],
                        "air_time": air
                    }

                mlp.put(por_aerolinea, code, reg)


    heap = pq.new_heap(is_min_pq=True)
    keys = mlp.key_set(por_aerolinea)

    for i in range(al.size(keys)):
        code = al.get_element(keys, i)
        reg = mlp.get(por_aerolinea, code)
        if reg["count"] > 0 and reg["best_flight"] is not None:
            prom_air = reg["sum_air"] / reg["count"]
            prom_dist = reg["sum_dist"] / reg["count"]

            bf = reg["best_flight"]
            resumen = {
                "codigo_aerolinea": reg["code"],
                "nombre_aerolinea": reg["name"],
                "vuelos_programados": reg["count"],
                "duracion_promedio_min": round(prom_air, 2),
                "distancia_promedio_millas": round(prom_dist, 2),
                "vuelo_menor_duracion": {
                    "id": bf["id"],
                    "codigo_vuelo": bf["flight"],
                    "fecha_hora_salida_programada": f'{bf["date"]} {bf["sched_dep_time"]}',
                    "origen": bf["origin"],
                    "destino": bf["dest"],
                    "duracion_min": round(bf["air_time"], 2)
                }
            }

            prioridad = (-reg["count"], reg["code"])  # min-heap → mayor count primero; empate por código asc
            pq.insert(heap, prioridad, resumen)

    seleccion = al.new_list()
    total_heap = pq.size(heap)
    extraer = n if total_heap >= n else total_heap

    for j in range(extraer):
        val = pq.remove(heap)
        al.add_last(seleccion, val)

    final = get_time()
    tiempo = delta_time(inicio, final)

    return tiempo, extraer, seleccion

def req_5(catalog, f_inicial, f_final, destino, n):
    
    inicio = get_time()
    flights = catalog["flights"]
    por_aerolinea = mlp.new_map(al.size(flights), 0.7)

    fecha_ini = datetime.strptime(f_inicial, "%Y-%m-%d")
    fecha_fin = datetime.strptime(f_final, "%Y-%m-%d")

    for i in range(al.size(flights)):
        v = al.get_element(flights, i)

        f_v = v["date"]
        
        if v["dest"] == destino and (fecha_ini <= f_v <= fecha_fin):
            t_sched = v["sched_arr_time"]
            t_real = v["arr_time"]

            sched_min = t_sched.hour * 60 + t_sched.minute
            real_min = t_real.hour * 60 + t_real.minute
         
            punt = real_min - sched_min
            
            if punt < -720:
                punt += 1440
            elif punt > 720:
                punt -= 1440

            code = v["carrier"]
            reg = mlp.get(por_aerolinea, code)
            
            if reg is None:
                reg = {
                    "code": code,
                    "name": v["name"],
                    "sum_punt": 0.0,
                    "count": 0,
                    "sum_air": 0.0,
                    "sum_dist": 0.0,
                    "max_dist": -1.0,
                    "max_flight": None
                }

            reg["sum_punt"] += punt
            reg["count"] += 1
           
            reg["sum_air"] += v["air_time"]
            dist_v = v["distance"]
            reg["sum_dist"] += dist_v

            if dist_v > reg["max_dist"]:
                reg["max_dist"] = dist_v
                reg["max_flight"] = {
                    "id": v["id"],
                    "flight": v["flight"],
                    "date": v["date"].strftime("%Y-%m-%d"),
                    "arr_time": v["arr_time"].strftime("%H:%M"),
                    "origin": v["origin"],
                    "dest": v["dest"],
                    "air_time": v["air_time"]
                }

            mlp.put(por_aerolinea, code, reg)

    heap = pq.new_heap(is_min_pq=True)
    keys = mlp.key_set(por_aerolinea)

    for i in range(al.size(keys)):
        code = al.get_element(keys, i)
        reg = mlp.get(por_aerolinea, code)
        
        if reg["count"] > 0 and reg["max_flight"] is not None:
            prom_punt = reg["sum_punt"] / reg["count"]
            prom_air  = reg["sum_air"] / reg["count"] if reg["count"] > 0 else 0.0
            prom_dist = reg["sum_dist"] / reg["count"] if reg["count"] > 0 else 0.0

            mf = reg["max_flight"]
            resumen = {
                "codigo_aerolinea": reg["code"],
                "nombre_aerolinea": reg["name"],
                "vuelos_analizados": reg["count"],
                "duracion_promedio_min": round(prom_air, 2),
                "distancia_promedio_millas": round(prom_dist, 2),
                "puntualidad_promedio_min": round(prom_punt, 2),
                "vuelo_mayor_distancia": {
                    "id": mf["id"],
                    "codigo_vuelo": mf["flight"],
                    "fecha_hora_llegada": f'{mf["date"]} {mf["arr_time"]}',
                    "origen": mf["origin"],
                    "destino": mf["dest"],
                    "duracion_min": round(mf["air_time"], 2)
                }
            }

            # Prioridad: (|promedio_puntualidad|, code) → más cercano a 0 primero; empate por código
            prioridad = (abs(prom_punt), reg["code"])
            pq.insert(heap, prioridad, resumen)

    seleccion = al.new_list()
    total_heap = pq.size(heap)
    extraer = min(n, total_heap)

    for j in range(extraer):
        val = pq.remove(heap)
        al.add_last(seleccion, val)

    final = get_time()
    tiempo = delta_time(inicio, final)

    return tiempo, extraer, seleccion

def req_6(catalog,f_inicial, f_final, d_min, d_max, m):
       
    inicio = get_time()
    flights = catalog["flights"]

    por_aerolinea = mlp.new_map(al.size(flights), 0.7)

    fecha_ini = datetime.strptime(f_inicial, "%Y-%m-%d")
    fecha_fin = datetime.strptime(f_final, "%Y-%m-%d")

    for i in range(al.size(flights)):
        v = al.get_element(flights, i)

        f_v = v["date"]
        dist = v["distance"]

        if (fecha_ini <= f_v <= fecha_fin) and (d_min <= dist <= d_max):
            sched_dep = v["sched_dep_time"]
            real_dep = v["dep_time"]

            sched_min = sched_dep.hour * 60 + sched_dep.minute
            real_min = real_dep.hour * 60 + real_dep.minute

            diff = real_min - sched_min

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
                "date": v["date"].strftime("%Y-%m-%d"),
                "dep_time": v["dep_time"].strftime("%H:%M"),
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
                "nombre_aerolinea": reg["name"],
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

            # La clave es (desviación_estándar, promedio) para ordenar
            # primero por estabilidad, luego por promedio en caso de empate
            pq.insert(heap, (sd, mu), resumen)

    # Extraer las M aerolíneas
    aerolineas = al.new_list()
    total_heap = pq.size(heap)
    extraer = min(m, total_heap)

    for j in range(extraer):
        val = pq.remove(heap)
        al.add_last(aerolineas, val)

    final = get_time()
    tiempo = delta_time(inicio, final)

    return tiempo, extraer, aerolineas


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
