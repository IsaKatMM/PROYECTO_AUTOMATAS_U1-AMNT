"""
Módulo: monitor.py
Descripción: Lógica del monitor de bitácoras de delivery. Lee los archivos CSV,
             agrupa los eventos por sesión, ejecuta las transiciones del 
             AFD Mínimo de 9 estados y genera el reporte con la matriz de confusión.
Asignatura: Teoría de Autómatas y Computabilidad Avanzada (UNL)
"""

import csv
import time
import os
from automata import EvaluadorAutomatas

class MonitorBitacoras:
    def __init__(self):
        self.evaluador = EvaluadorAutomatas()

    def procesar_archivo(self, ruta_csv):
        """
        Lee una bitácora CSV, agrupa las transiciones por id_sesion,
        ejecuta la simulación formal del autómata y calcula las métricas.
        """
        if not os.path.exists(ruta_csv):
            raise FileNotFoundError(f"El archivo '{ruta_csv}' no existe.")

        sesiones = {}
        etiquetas_reales = {}
        
        inicio_tiempo = time.perf_counter()

        # 1. Lectura del archivo CSV y reconstrucción de cadenas por sesión
        with open(ruta_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for fila in reader:
                s_id = fila['id_sesion']
                simbolo = fila['simbolo']
                
                if s_id not in sesiones:
                    sesiones[s_id] = []
                    # Si el archivo contiene la columna etiqueta (ej. validacion.csv), la almacenamos
                    if 'etiqueta' in fila and fila['etiqueta']:
                        etiquetas_reales[s_id] = fila['etiqueta'].lower()
                        
                sesiones[s_id].append(simbolo)

        # Contadores de la Matriz de Confusión
        vp = 0  # Verdaderos Positivos (Anómala predicha como anómala)
        fp = 0  # Falsos Positivos     (Normal predicha como anómala)
        fn = 0  # Falsos Negativos     (Anómala predicha como normal)
        vn = 0  # Verdaderos Negativos (Normal predicha como normal)
        
        resultados_sesiones = []

        # 2. Auditoría sesión por sesión utilizando el AFD Mínimo
# 2. Auditoría sesión por sesión utilizando el AFD Mínimo
        for s_id, cadena in sesiones.items():
            etiqueta_pred, patron_det = self.evaluador.evaluar_cadena(cadena)
            
            resultados_sesiones.append({
                "id_sesion": s_id,
                "cadena": "".join(cadena),
                "prediccion": etiqueta_pred,
                "patron": patron_det
            })
            
            if s_id in etiquetas_reales:
                real = etiquetas_reales[s_id].strip().lower()
                # Normalizar la etiqueta real (quitar tildes para evitar errores de coincidencia)
                real_normalizada = real.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                pred_normalizada = etiqueta_pred.strip().lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                
                if real_normalizada == "anomala" and pred_normalizada == "anomala":
                    vp += 1
                elif real_normalizada == "normal" and pred_normalizada == "anomala":
                    fp += 1
                elif real_normalizada == "anomala" and pred_normalizada == "normal":
                    fn += 1
                elif real_normalizada == "normal" and pred_normalizada == "normal":
                    vn += 1

        fin_tiempo = time.perf_counter()
        tiempo_ejecucion_ms = (fin_tiempo - inicio_tiempo) * 1000

        # 3. Cálculo de métricas derivadas (Precisión y Exhaustividad)
        precision = (vp / (vp + fp)) if (vp + fp) > 0 else 0.0
        exhaustividad = (vp / (vp + fn)) if (vp + fn) > 0 else 0.0

        reporte = {
            "total_sesiones": len(sesiones),
            "tiempo_ms": tiempo_ejecucion_ms,
            "vp": vp,
            "fp": fp,
            "fn": fn,
            "vn": vn,
            "precision": precision,
            "exhaustividad": exhaustividad,
            "tiene_etiquetas": len(etiquetas_reales) > 0,
            "detalles": resultados_sesiones
        }

        return reporte


if __name__ == "__main__":
    # Prueba rápida ejecutando monitor.py por consola
    monitor = MonitorBitacoras()
    
    # Buscar el archivo de validación en rutas comunes
    rutas_posibles = ["validacion.csv", os.path.join("..", "datos", "validacion.csv"), "datos/validacion.csv"]
    ruta_encontrada = None
    for r in rutas_posibles:
        if os.path.exists(r):
            ruta_encontrada = r
            break
            
    if ruta_encontrada:
        try:
            rep = monitor.procesar_archivo(ruta_encontrada)
            print("==========================================================================")
            print("               REPORTE DE MONITOR POR CONSOLA (AFD MÍNIMO)                ")
            print("==========================================================================")
            print(f"  • Total de Sesiones Auditadas : {rep['total_sesiones']}")
            print(f"  • Tiempo de Procesamiento     : {rep['tiempo_ms']:.3f} ms")
            if rep['tiene_etiquetas']:
                print(f"  • Verdaderos Positivos (VP)   : {rep['vp']}")
                print(f"  • Falsos Positivos (FP)       : {rep['fp']}")
                print(f"  • Falsos Negativos (FN)       : {rep['fn']}")
                print(f"  • Verdaderos Negativos (VN)   : {rep['vn']}")
                print(f"  • Precisión                   : {rep['precision']:.2%}")
                print(f"  • Exhaustividad (Recall)      : {rep['exhaustividad']:.2%}")
            print("==========================================================================")
        except Exception as e:
            print(f"Error al ejecutar el monitor: {e}")
    else:
        print("⚠️ No se encontró ningún archivo CSV de validación para la prueba rápida.")