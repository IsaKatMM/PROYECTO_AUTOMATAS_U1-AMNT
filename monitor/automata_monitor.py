"""
Módulo: interfaz_automata.py
Descripción: Interfaz gráfica interactiva con simulación paso a paso 
             y tabla de transiciones del AFD Mínimo (9 Estados).
             Se alimenta directamente de 'automata.py'.
Asignatura: Teoría de Autómatas y Computabilidad Avanzada (UNL)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from automata import AFDMínimo, EvaluadorAutomatas

class InterfazSimuladorAutomata:
    def __init__(self, root):
        self.root = root
        self.root.title("UNL - Visualizador Formal y Simulación del AFD Mínimo (9 Estados)")
        self.root.geometry("850x650")
        self.root.config(bg="#f8f9fa")
        
        # Importar la lógica pura desde automata.py
        self.afd = AFDMínimo()
        self.evaluador = EvaluadorAutomatas()
        
        # Encabezado
        header = tk.Label(
            root, 
            text="SISTEMA DE MONITOREO Y AUDITORÍA - AFD MÍNIMO (DELTA TEAM)", 
            font=("Helvetica", 14, "bold"), 
            bg="#1e3d59", 
            fg="white",
            padx=10,
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Notebook (Pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Pestaña 1: Trazador en Vivo paso a paso
        self.tab_traza = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_traza, text=" 🔍 Simulación y Traza ")
        self.crear_pestana_traza()
        
        # Pestaña 2: Tabla de Transiciones δ(q, a)
        self.tab_tabla = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_tabla, text=" 📊 Tabla de Transiciones δ (9 Estados) ")
        self.crear_pestana_tabla()

    # ------------------------------------------------------------------
    # PESTAÑA 1: TRAZA PASO A PASO
    # ------------------------------------------------------------------
    def crear_pestana_traza(self):
        frame = ttk.LabelFrame(self.tab_traza, text=" Entrada de Cadena de Eventos ", padding=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        lbl_info = tk.Label(
            frame, 
            text="Ingrese una cadena con símbolos del alfabeto Σ = {P, A, R, S, E, C, L}:\n"
                 "• Normal: PARSE | PARSEL\n"
                 "• Doble Pago P1: PAARSE\n"
                 "• Anomalías de Flujo (q8): PE (Entrega sin S) o PARSC (Cancelación tras S)", 
            font=("Consolas", 9), 
            justify=tk.LEFT,
            fg="#495057"
        )
        lbl_info.pack(anchor=tk.W, pady=5)
        
        subframe = ttk.Frame(frame)
        subframe.pack(fill=tk.X, pady=10)
        
        ttk.Label(subframe, text="Cadena (w): ", font=("Helvetica", 11, "bold")).pack(side=tk.LEFT)
        self.ent_cadena = ttk.Entry(subframe, font=("Consolas", 12, "bold"), width=28)
        self.ent_cadena.pack(side=tk.LEFT, padx=10)
        self.ent_cadena.focus()
        
        btn_simular = ttk.Button(subframe, text="Simular en AFD", command=self.ejecutar_simulacion)
        btn_simular.pack(side=tk.LEFT)
        
        self.lbl_veredicto = tk.Label(
            frame, 
            text="Esperando ingreso de secuencia...", 
            font=("Helvetica", 11, "bold"), 
            bg="#e9ecef", 
            fg="#212529", 
            relief=tk.GROOVE,
            padx=10,
            pady=10
        )
        self.lbl_veredicto.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame, text="Traza paso a paso del recorrido δ(q_actual, símbolo):", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(5,0))
        
        self.txt_traza = tk.Text(frame, font=("Consolas", 10), height=12, bg="#1e1e1e", fg="#d4d4d4", wrap=tk.WORD)
        self.txt_traza.pack(fill=tk.BOTH, expand=True, pady=5)

    def ejecutar_simulacion(self):
        cadena = self.ent_cadena.get().strip().upper()
        if not cadena:
            messagebox.showwarning("Atención", "Por favor ingrese una secuencia de símbolos.")
            return
            
        etiqueta, patron, historial = self.afd.simular_cadena(list(cadena))
        
        self.txt_traza.delete(1.0, tk.END)
        self.txt_traza.insert(tk.END, f"=== INICIANDO SIMULACIÓN SOBRE EL AFD MÍNIMO (9 ESTADOS) ===\n")
        self.txt_traza.insert(tk.END, f"Cadena evaluada : w = {cadena}\n")
        self.txt_traza.insert(tk.END, f"Estado Inicial  : {self.afd.q0}\n")
        self.txt_traza.insert(tk.END, "-"*50 + "\n\n")
        
        q_act = self.afd.q0
        paso = 1
        for sim in cadena:
            if sim not in self.afd.alfabeto:
                self.txt_traza.insert(tk.END, f"Paso {paso}: Símbolo '{sim}' fuera de Σ -> Se ignora.\n")
                continue
                
            q_sig = self.afd.delta.get(q_act, {}).get(sim, 'q8')
            self.txt_traza.insert(tk.END, f"Paso {paso}: δ({q_act}, '{sim}') ──> {q_sig}\n")
            q_act = q_sig
            paso += 1
            if q_act == 'q8':
                self.txt_traza.insert(tk.END, f"\n⚠️ ¡Se alcanzó el Estado Trampa de Anomalía 'q8'! Deteniendo simulación.\n")
                break
                
        self.txt_traza.insert(tk.END, "\n" + "="*50 + "\n")
        self.txt_traza.insert(tk.END, f"Camino de Estados: {' -> '.join(historial)}\n")
        
        if etiqueta == "anómala":
            res_txt = f"❌ VEREDICTO: ANÓMALA | Patrón Detectado / Estado Final: {patron} ({q_act})"
            bg_col, fg_col = "#f8d7da", "#721c24"
        else:
            res_txt = f"✅ VEREDICTO: NORMAL | Flujo Correcto"
            bg_col, fg_col = "#d4edda", "#155724"
            
        self.lbl_veredicto.config(text=res_txt, bg=bg_col, fg=fg_col)

    # ------------------------------------------------------------------
    # PESTAÑA 2: TABLA DE TRANSICIONES FORMAL (TABLA 7)
    # ------------------------------------------------------------------
    def crear_pestana_tabla(self):
        frame = ttk.LabelFrame(self.tab_tabla, text=" Matriz de Transición δ(q, a) - Tabla 7 del Informe ", padding=15)
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        cols = ["Estado"] + sorted(list(self.afd.alfabeto)) + ["Tipo / Descripción (Tabla 6)"]
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=75, anchor=tk.CENTER)
        tree.column("Estado", width=80)
        tree.column("Tipo / Descripción (Tabla 6)", width=220, anchor=tk.W)
        
        descripciones = {
            'q0': "Estado inicial de la sesión",
            'q1': "Vigila cancelación tras Asignación (S)",
            'q2': "Se leyó un primer pago A (sin S previa)",
            'q3': "Final: Doble Pago (AA) sin S previa",
            'q4': "3 o más A seguidas (sin S previa)",
            'q5': "3 o más A seguidas (tras S previa)",
            'q6': "Se leyó un primer pago A (tras S previa)",
            'q7': "Final: Doble Pago (AA) con S previa",
            'q8': "Final: Macro-estado trampa de anomalías (E sin S, SC)"
        }
        
        for q in ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8']:
            row = [q]
            for sim in sorted(list(self.afd.alfabeto)):
                dest = self.afd.delta.get(q, {}).get(sim, '-')
                row.append(dest)
                
            row.append(descripciones.get(q, ""))
            tree.insert("", tk.END, values=row)
            
        tree.pack(fill=tk.BOTH, expand=True, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazSimuladorAutomata(root)
    root.mainloop()