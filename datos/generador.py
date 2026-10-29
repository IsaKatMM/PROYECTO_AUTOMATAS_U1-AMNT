import csv
import random
import os
import importlib

# importar kagglehub para descarga automatica
try:
    kagglehub = importlib.import_module("kagglehub")
    KaggleDatasetAdapter = kagglehub.KaggleDatasetAdapter
    USAR_KAGGLEHUB = True
except ImportError:
    USAR_KAGGLEHUB = False


# 1. Obtener IDs reales desde Kaggle
ids_reales = []
actores_reales = []

if USAR_KAGGLEHUB:
    try:
        print("Descargando dataset de base desde Kaggle (gauravmalik26/food-delivery-dataset)...")
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "gauravmalik26/food-delivery-dataset",
            ""
        )
        posibles_cols_id = ["ID", "Order_ID", "index", "Order_No", "Order ID"]
        posibles_cols_actor = ["Delivery_person_ID", "Customer_ID", "Agent_ID"]
        
        col_id = next((col for col in posibles_cols_id if col in df.columns), df.columns[0])
        col_actor = next((col for col in posibles_cols_actor if col in df.columns), df.columns[1] if len(df.columns) > 1 else df.columns[0])
        
        ids_reales = df[col_id].dropna().astype(str).tolist()
        actores_reales = df[col_actor].dropna().astype(str).tolist()
        print("¡IDs reales extraídos con éxito de Kaggle!")
    except Exception as e:
        print(f"Aviso al conectar con Kagglehub: {e}. Usando respaldo local/sintético de IDs.")

#Configuración con semilla fija
SEED = 42
random.seed(SEED)

# Alfabeto pedidos de comida a domicilio
DICCIONARIO_ALFABETO = {
    "P": "PEDIR",
    "A": "PAGAR",
    "R": "PREPARAR",
    "S": "ASIGNAR",
    "E": "ENTREGAR",
    "C": "CANCELAR",
    "L": "CALIFICAR"  # evento irrelevante 
}

def evaluar_patron_cadena(cadena_simbolos):
    """Evalúa los patrones formales de la propuesta sobre la cadena de eventos."""
    texto = "".join(cadena_simbolos)
    
    # P1: Anomala -> Doble pago consecutivo (AA)
    if "AA" in texto:
        return "anomala", "P1"
    
    # P2: Anomala -> Entrega (E) sin Asignación previa (S)
    if "E" in texto:
        pos_e = texto.find("E")
        pos_s = texto.find("S")
        if pos_s == -1 or pos_s > pos_e:
            return "anomala", "P2"
            
    # P4: Anomala -> Asignación y cancelación inmediata (SC)
    if "SC" in texto:
        return "anomala", "P4"
        
    # P3: Validación -> Flujo correcto (ARS)
    if "ARS" in texto:
        return "normal", "P3"
        
    return "normal", "NINGUNO"

print("Mapeando identificadores y generando bitacoras...")

# Generar 320 validaciones y 60 pruebas
total_sesiones_val = 320
total_sesiones_prueba = 60
total_pedidos = total_sesiones_val + total_sesiones_prueba

sesiones_procesadas = []
for i in range(1, total_pedidos + 1):
    id_sesion = f"S-{ids_reales[(i-1) % len(ids_reales)]}" if ids_reales else f"S-{1000+i:04d}"
    actor = actores_reales[(i-1) % len(actores_reales)] if actores_reales else f"USR-{random.randint(100, 999)}"
    
    # Control de porcentaje de anomalias (15% a 20%)
    prob = random.random()
    if prob < 0.18: 
        patron_inyectado = random.choice(["AA", "SIN_S", "SC"])
        if patron_inyectado == "AA": secuencia = ["P", "A", "A", "R", "S", "E"]
        elif patron_inyectado == "SIN_S": secuencia = ["P", "A", "R", "E"]
        else: secuencia = ["P", "A", "R", "S", "C"]
    elif prob < 0.28: # Casos casi anomalos o de variación
        secuencia = random.choice([["P", "A", "L", "R", "S"], ["P", "A", "R", "S", "L", "E"]])
    else:
        secuencia = ["P", "A", "R", "S", "E"]
        
    # Inyectar eventos irrelevantes 'L' (CALIFICAR) 
    secuencia_final = []
    for s in secuencia:
        secuencia_final.append(s)
        if random.random() < 0.3:
            secuencia_final.append("L")
            
    etiqueta, tipo_patron = evaluar_patron_cadena(secuencia_final)
    
    sesiones_procesadas.append({
        "id_sesion": id_sesion,
        "actor": actor,
        "cadena": secuencia_final,
        "etiqueta": etiqueta,
        "tipo_patron": tipo_patron
    })

# Separar en archivos de validación y de prueba
val_sesiones = sesiones_procesadas[:total_sesiones_val]
prueba_sesiones = sesiones_procesadas[total_sesiones_val:]

id_evento = 1000

# Asegurar que la carpeta actual guarde los archivos correctamente
os.makedirs(".", exist_ok=True)

# 1. Escritura de 'validacion.csv'
with open("validacion.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id_evento", "fecha_hora", "id_sesion", "actor", "evento", "simbolo", "etiqueta", "tipo_patron"])
    for s in val_sesiones:
        for idx, sim in enumerate(s["cadena"]):
            id_evento += 1
            writer.writerow([id_evento, f"2026-10-20 10:{idx:02d}:15", s["id_sesion"], s["actor"], DICCIONARIO_ALFABETO[sim], sim, s["etiqueta"], s["tipo_patron"]])

# 2. Escritura de 'prueba.csv' y 'prueba_clave.csv'
with open("prueba.csv", mode="w", newline="", encoding="utf-8") as f_p, open("prueba_clave.csv", mode="w", newline="", encoding="utf-8") as f_c:
    writer_p = csv.writer(f_p)
    writer_c = csv.writer(f_c)
    writer_p.writerow(["id_evento", "fecha_hora", "id_sesion", "actor", "evento", "simbolo"])
    writer_c.writerow(["id_sesion", "etiqueta", "tipo_patron"])
    
    for s in prueba_sesiones:
        writer_c.writerow([s["id_sesion"], s["etiqueta"], s["tipo_patron"]])
        for idx, sim in enumerate(s["cadena"]):
            id_evento += 1
            writer_p.writerow([id_evento, f"2026-10-20 11:{idx:02d}:30", s["id_sesion"], s["actor"], DICCIONARIO_ALFABETO[sim], sim])

print("-------------------------------------------------------------------------")
print(" - validacion.csv")
print(" - prueba.csv")
print(" - prueba_clave.csv")
print("-------------------------------------------------------------------------")