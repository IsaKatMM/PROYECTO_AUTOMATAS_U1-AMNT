"""
Módulo: interfaz_monitor.py
Descripción: Interfaz gráfica para la carga, auditoría masiva de archivos CSV 
             y cálculo de métricas de desempeño (Matriz de Confusión).
             Se alimenta de 'monitor.py' y del AFD Mínimo de 9 estados.
Asignatura: Teoría de Autómatas y Computabilidad Avanzada (UNL)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from monitor import MonitorBitacoras

class InterfazMonitorCSV:
    def __init__(self, root):
        self.root = root
        self.root.title("UNL - Monitor de Auditoría de Bitácoras CSV (AFD Mínimo)")
        self.root.geometry("900x680")
        self.root.config(bg="#f8f9fa")
        
        self.motor_monitor = MonitorBitacoras()
        
        # Encabezado
        header = tk.Label(
            root, 
            text="AUDITORÍA AUTOMATIZADA DE BITÁCORAS - DELTA TEAM", 
            font=("Helvetica", 14, "bold"), 
            bg="#1e3d59", 
            fg="white",
            padx=10,
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Panel Principal
        main_frame = ttk.Frame(root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botonera superior
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.btn_cargar = ttk.Button(btn_frame, text="📁 Seleccionar y Auditar Archivo CSV", command=self.cargar_csv)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)
        
        self.lbl_ruta = ttk.Label(btn_frame, text="Ningún archivo seleccionado", font=("Consolas", 9), foreground="#6c757d")
        self.lbl_ruta.pack(side=tk.LEFT, padx=10)
        
        # Área de Resultados (Texto con scroll)
        self.txt_resultados = tk.Text(main_frame, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", wrap=tk.WORD)
        self.txt_resultados.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Mensaje inicial instructivo para la defensa
        self.txt_resultados.insert(
            tk.END, 
            "=== INSTRUCCIONES PARA LA PRUEBA EN VIVO (DEFENSA) ===\n"
            "1. Haga clic en 'Seleccionar y Auditar Archivo CSV'.\n"
            "2. Elija 'validacion.csv' o el archivo 'prueba.csv' modificado por la docente.\n"
            "3. El sistema procesará las sesiones mediante el AFD Mínimo (9 estados), "
            "calculando la matriz de confusión, precisión, exhaustividad y el tiempo en milisegundos.\n"
        )

    def cargar_csv(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar bitácora CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return
            
        self.lbl_ruta.config(text=os.path.basename(ruta))
        
        try:
            # Ejecutar el procesamiento mediante monitor.py
            reporte = self.motor_monitor.procesar_archivo(ruta)
            
            # Mostrar resultados formateados en la consola visual
            self.txt_resultados.delete(1.0, tk.END)
            self.txt_resultados.insert(tk.END, f"=========================================================================\n")
            self.txt_resultados.insert(tk.END, f" REPORTE DE AUDITORÍA: {os.path.basename(ruta)}\n")
            self.txt_resultados.insert(tk.END, f"=========================================================================\n\n")
            self.txt_resultados.insert(tk.END, f"📊 Total de Sesiones Procesadas : {reporte['total_sesiones']}\n")
            self.txt_resultados.insert(tk.END, f"⏱️ Tiempo de Ejecución (AFD)   : {reporte['tiempo_ms']:.3f} ms\n\n")
            
            if reporte['tiene_etiquetas']:
                self.txt_resultados.insert(tk.END, "--- MATRIZ DE CONFUSIÓN Y MÉTRICAS ---\n")
                self.txt_resultados.insert(tk.END, f"  • Verdaderos Positivos (VP) : {reporte['vp']}\n")
                self.txt_resultados.insert(tk.END, f"  • Falsos Positivos (FP)     : {reporte['fp']}\n")
                self.txt_resultados.insert(tk.END, f"  • Falsos Negativos (FN)     : {reporte['fn']}\n")
                self.txt_resultados.insert(tk.END, f"  • Verdaderos Negativos (VN) : {reporte['vn']}\n")
                self.txt_resultados.insert(tk.END, f"  • Precisión                 : {reporte['precision']:.2%}\n")
                self.txt_resultados.insert(tk.END, f"  • Exhaustividad (Recall)   : {reporte['exhaustividad']:.2%}\n\n")
            else:
                self.txt_resultados.insert(tk.END, "ℹ️ Nota: Este archivo no contiene etiquetas (archivo ciego de prueba).\n")
                self.txt_resultados.insert(tk.END, "   Se muestran a continuación los veredictos emitidos por el AFD Mínimo:\n\n")
                
            self.txt_resultados.insert(tk.END, f"--- DETALLE DE DETECCIONES ({len(reporte['detalles'])}) ---\n")
            anomalias_encontradas = 0
            for item in reporte['detalles']:
                if item['prediccion'] == "anómala":
                    anomalias_encontradas += 1
                    self.txt_resultados.insert(
                        tk.END, 
                        f" [!] Sesión: {item['id_sesion']} | Cadena: {item['cadena']:<12} | Patrón: {item['patron']}\n"
                    )
            
            self.txt_resultados.insert(tk.END, f"\nTotal de anomalías detectadas por el monitor: {anomalias_encontradas}\n")
            
        except Exception as e:
            messagebox.showerror("Error de Procesamiento", f"Ocurrió un error al leer el archivo:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazMonitorCSV(root)
    root.mainloop()