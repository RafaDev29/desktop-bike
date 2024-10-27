# views/analysis_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.reports_controller import get_duracion_prestamos, get_ranking_clientes, get_preferencias_por_rodada, get_preferencias_por_color, get_preferencias_por_dia
import pandas as pd
import matplotlib.pyplot as plt

class AnalysisView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Análisis Descriptivo")
        self.geometry("750x600")
        self.configure(bg="#f0f4f7")

        title_label = tk.Label(self, text="Análisis Descriptivo", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#34495e")
        title_label.pack(pady=(10, 20))

        # Botones de análisis
        tk.Button(self, text="Duración de los Préstamos", command=self.show_duracion_prestamos).pack(pady=5)
        tk.Button(self, text="Ranking de Clientes", command=self.show_ranking_clientes).pack(pady=5)
        tk.Button(self, text="Preferencias por Rodada", command=self.show_preferencias_rodada).pack(pady=5)
        tk.Button(self, text="Preferencias por Color", command=self.show_preferencias_color).pack(pady=5)
        tk.Button(self, text="Preferencias por Día de la Semana", command=self.show_preferencias_dia).pack(pady=5)

        # Botón para exportar datos
        tk.Button(self, text="Exportar a CSV", command=self.export_to_csv).pack(pady=10)
        tk.Button(self, text="Exportar a Excel", command=self.export_to_excel).pack(pady=10)

        self.data = None

    def show_duracion_prestamos(self):
        stats = get_duracion_prestamos()
        if stats:
            stats_text = (
                f"Media: {stats['media']:.2f}\n"
                f"Mediana: {stats['mediana']}\n"
                f"Moda: {stats['moda']}\n"
                f"Mínimo: {stats['minimo']}\n"
                f"Máximo: {stats['maximo']}\n"
                f"Desviación Estándar: {stats['desviacion']:.2f}\n"
                f"Cuartiles: {stats['cuartiles']}"
            )
            messagebox.showinfo("Duración de los Préstamos", stats_text)
        else:
            messagebox.showinfo("Duración de los Préstamos", "No hay datos disponibles.")
    
    def show_ranking_clientes(self):
        ranking = get_ranking_clientes()
        self.data = pd.DataFrame(ranking, columns=["Clave", "Nombre", "Teléfono", "Cantidad de Préstamos"])
        self.show_data_in_treeview(self.data)
    
    def show_preferencias_rodada(self):
        preferencias = get_preferencias_por_rodada()
        self.data = pd.DataFrame(preferencias, columns=["Rodada", "Cantidad de Préstamos"])
        self.show_data_in_treeview(self.data)
        self.data.plot.pie(y="Cantidad de Préstamos", labels=self.data["Rodada"], autopct="%1.1f%%", legend=False)
        plt.title("Preferencias por Rodada")
        plt.show()
    
    def show_preferencias_color(self):
        preferencias = get_preferencias_por_color()
        self.data = pd.DataFrame(preferencias, columns=["Color", "Cantidad de Préstamos"])
        self.show_data_in_treeview(self.data)
        self.data.plot.pie(y="Cantidad de Préstamos", labels=self.data["Color"], autopct="%1.1f%%", legend=False)
        plt.title("Preferencias por Color")
        plt.show()

    def show_preferencias_dia(self):
        preferencias = get_preferencias_por_dia()
        self.data = pd.DataFrame(preferencias, columns=["Día de la Semana", "Cantidad de Préstamos"])
        self.show_data_in_treeview(self.data)
        self.data.plot.bar(x="Día de la Semana", y="Cantidad de Préstamos", legend=False)
        plt.title("Preferencias por Día de la Semana")
        plt.show()

    def show_data_in_treeview(self, dataframe):
        if hasattr(self, 'tree'):
            self.tree.destroy()

        self.tree = ttk.Treeview(self, show="headings", columns=dataframe.columns)
        for col in dataframe.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        for row in dataframe.itertuples(index=False):
            self.tree.insert("", "end", values=row)
        self.tree.pack(pady=10, fill="both", expand=True)

    def export_to_csv(self):
        if self.data is not None:
            self.data.to_csv("reporte.csv", index=False)
            messagebox.showinfo("Exportar CSV", "Reporte exportado como reporte.csv.")
        else:
            messagebox.showerror("Error", "No hay datos para exportar.")
    
    def export_to_excel(self):
        if self.data is not None:
            self.data.to_excel("reporte.xlsx", index=False)
            messagebox.showinfo("Exportar Excel", "Reporte exportado como reporte.xlsx.")
        else:
            messagebox.showerror("Error", "No hay datos para exportar.")
