"""
Módulo: automata.py
Descripción: Implementación formal del AFD Mínimo de 9 estados adaptado 
             estrictamente a la Tabla 7 y calibrado para 0 Falsos Positivos.
Asignatura: Teoría de Autómatas y Computabilidad Avanzada (UNL)
"""

class AFDMínimo:
    def __init__(self):
        # 1. Alfabeto formal Σ = {P, A, R, S, E, C, L}
        self.alfabeto = {'P', 'A', 'R', 'S', 'E', 'C', 'L'}
        
        # 2. Conjunto de Estados Q del AFD Mínimo (9 Estados exactos de la Tabla 7)
        self.Q = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8'}
        
        # 3. Estado Inicial q0
        self.q0 = 'q0'
        
        # 4. Estados Finales / De Aceptación F 
        self.F = {
            'q3': ('anómala', 'P1'),
            'q7': ('anómala', 'P1'),
            'q8': ('anómala', 'ANOMALIA_FLUJO')
        }
        
        # 5. Función de Transición determinista δ(q, a) -> q' 
        self.delta = {
            'q0': {
                'P': 'q0', 'R': 'q0', 'L': 'q0', 'A': 'q2', 'S': 'q1', 'E': 'q8', 'C': 'q0'
            },
            'q1': {
                'P': 'q0', 'R': 'q0', 'L': 'q0', 'A': 'q6', 'S': 'q1', 'E': 'q0', 'C': 'q8'
            },
            'q2': {
                'P': 'q0', 'R': 'q0', 'L': 'q0', 'A': 'q3', 'S': 'q1', 'E': 'q8', 'C': 'q0'
            },
            'q3': {
                'P': 'q8', 'R': 'q8', 'L': 'q8', 'A': 'q4', 'S': 'q8', 'E': 'q8', 'C': 'q8'
            },
            'q4': {
                'P': 'q0', 'R': 'q0', 'L': 'q0', 'A': 'q4', 'S': 'q1', 'E': 'q8', 'C': 'q0'
            },
            'q5': {
                'P': 'q0', 'R': 'q0', 'L': 'q0', 'A': 'q5', 'S': 'q1', 'E': 'q0', 'C': 'q0'
            },
            'q6': {
                'P': 'q0', 'R': 'q0', 'L': 'q0', 'A': 'q7', 'S': 'q1', 'E': 'q0', 'C': 'q0'
            },
            'q7': {
                'P': 'q8', 'R': 'q8', 'L': 'q8', 'A': 'q5', 'S': 'q8', 'E': 'q8', 'C': 'q8'
            },
            'q8': {
                'P': 'q8', 'R': 'q8', 'L': 'q8', 'A': 'q8', 'S': 'q8', 'E': 'q8', 'C': 'q8'
            }
        }

    def simular_cadena(self, cadena):
            """
            Simula formalmente el recorrido de una cadena de símbolos sobre el AFD Mínimo.
            Retorna: (etiqueta, patron_detectado, historial_estados)
            """
            estado_actual = self.q0
            historial = [estado_actual]
            
            patron_detectado = "NINGUNO"
            es_anomala = False
            
            for simbolo in cadena:
                simbolo = simbolo.upper()
                if simbolo not in self.alfabeto:
                    continue
                    
                estado_anterior = estado_actual
                estado_actual = self.delta.get(estado_actual, {}).get(simbolo, 'q8')
                historial.append(estado_actual)
                
                # Identificar qué regla o patrón específico disparó la anomalía
                if estado_actual in ('q3', 'q7'):
                    patron_detectado = 'P1'
                    es_anomala = True
                elif estado_anterior == 'q0' and simbolo == 'E' and estado_actual == 'q8':
                    patron_detectado = 'P2'
                    es_anomala = True
                elif estado_anterior == 'q1' and simbolo == 'C' and estado_actual == 'q8':
                    patron_detectado = 'P4'
                    es_anomala = True
                elif estado_anterior in ('q3', 'q7') and estado_actual == 'q8':
                    patron_detectado = 'P1'
                    es_anomala = True

            # Veredicto final basado en el estado o el patrón detectado
            if es_anomala or estado_actual in ('q3', 'q7', 'q8'):
                if not es_anomala and estado_actual == 'q8':
                    patron_detectado = 'P2_P4' # Resguardo general si cae en trampa
                return 'anómala', patron_detectado, historial
            else:
                return 'normal', 'NINGUNO', historial


class EvaluadorAutomatas:
    """Clase wrapper para integrar el autómata con el monitor de archivos CSV."""
    def __init__(self):
        self.afd = AFDMínimo()
        self.alfabeto = self.afd.alfabeto

    def evaluar_cadena(self, cadena):
        etiqueta, patron, _ = self.afd.simular_cadena(cadena)
        return etiqueta, patron


if __name__ == "__main__":
    afd = AFDMínimo()
    cadenas_prueba = [
        ("PARSEL", "Flujo Normal"),
        ("PAARSE", "Doble Pago P1"),
        ("PE", "Entrega sin Asignación P2"),
        ("PARSC", "Cancelación tras Asignación P4")
    ]
    
    print("=== SIMULACIÓN FORMAL AFD MÍNIMO (CALIBRADO) ===")
    for c, desc in cadenas_prueba:
        etiq, pat, hist = afd.simular_cadena(list(c))
        print(f"Cadena: {c:<7} | Desc: {desc:<28} | Traza: {' -> '.join(hist)}")
        print(f"         └─ Verificado: {etiq} ({pat})\n")