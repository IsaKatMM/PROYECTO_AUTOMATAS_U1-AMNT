**Δ TEAM**

# PROYECTO_AUTOMATAS_U1-AMNT

ABP sobre un monitor de secuencias en Python respaldado por Autómatas Finitos (AFND, AFD y AFD Mínimo) para vigilar las bitácoras y detectar anomalías o flujos correctos en una plataforma de entregas a domicilio.

## 👥 Autores
* **Josue Nathanael Asanza Abad**
* **Kevin Joel Nole Cabrera**
* **Cristian Abraham Tomalá González** 
* **Isabel Katherine Morocho Marizaca**
* **Docente:** Ing. Genoveva Suing[cite: 2]

---

## 📋 Descripción del Modelo Formal

El sistema procesa transacciones basadas en un alfabeto de 7 eventos ($\Sigma$)[cite: 3]:

* **P** - PEDIR: El cliente solicita el pedido[cite: 3].
* **A** - PAGAR: El cliente efectúa el pago[cite: 3].
* **R** - PREPARAR: El restaurante acepta y prepara la comida[cite: 3].
* **S** - ASIGNAR: Se asigna un repartidor al pedido[cite: 3].
* **E** - ENTREGAR: El repartidor entrega el pedido[cite: 3].
* **C** - CANCELAR: El pedido es cancelado[cite: 3].
* **L** - CALIFICAR: El cliente registra una reseña[cite: 3].

### Patrones Evaluados:
1. **P1 (Anomalía - Doble pago consecutivo):** Detecta dos cobros/pagos consecutivos (AA) sin evento intermedio.
2. **P2 (Anomalía - Entrega sin asignación previa):** Detecta entregas (E) sin que se haya asignado un repartidor (S) previamente[cite: 4].
3. **P3 (Validación - Flujo correcto):** Valida la secuencia correcta de pago, preparación y asignación (A-R-S)[cite: 4].
4. **P4 (Anomalía - Cancelación inmediata tras asignación):** Detecta cuando se asigna un repartidor y se cancela de inmediato (SC)[cite: 4].

---

## 🗂️ Estructura del Repositorio

Puedes organizar tus archivos del proyecto (scripts de Python, archivos CSV de pruebas, diseños de JFLAP, etc.) dentro de este repositorio de la siguiente manera:

```text
PROYECTO_AUTOMATAS_U1-AMNT/
│
├── datos/
│   └── prueba.csv              # Dataset de sesiones extraídas de Kaggle[cite: 4, 5]
├── src/
│   └── monitor.py              # Script principal en Python para el monitoreo
├── jflap/
│   └── automatas.jff           # Diseños y conversiones de autómatas en JFLAP
└── README.md

## ⚙️ Requisitos
Lenguaje: Python 3.x[cite: 3]

Herramientas de Diseño: JFLAP para la construcción de AFND, subconjuntos, AFD mínimo y minimización.

Entorno de desarrollo: Visual Studio Code[cite: 4].