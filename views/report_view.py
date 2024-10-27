# views/report_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.reports_controller import get_all_clients, get_all_units, get_retrasos, get_prestamos_por_retornar, get_prestamos_por_periodo
from datetime import datetime

class ReportView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Informes y Reportes")
        self.geometry("700x600")
        self.configure(bg="#f0f4f7")

        title_label = tk.Label(self, text="Informes y Reportes", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#34495e")
        title_label.pack(pady=(10, 20))

        # Menú de selección de tipo de reporte
        options_frame = tk.Frame(self, bg="#f0f4f7")
        options_frame.pack(pady=10)

        tk.Label(options_frame, text="Seleccionar reporte:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5)
        self.reporte_var = tk.StringVar(value="Clientes")
        report_menu = ttk.Combobox(options_frame, textvariable=self.reporte_var, values=["Clientes", "Unidades", "Retrasos", "Préstamos por Retornar (Período)", "Préstamos por Período"], font=("Helvetica", 12), state="readonly")
        report_menu.grid(row=0, column=1, padx=10, pady=5)

        # Campos de fecha para reportes de períodos usando DateEntry
        tk.Label(options_frame, text="Fecha Inicio:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5)
        self.fecha_inicio_entry = DateEntry(options_frame, width=12, font=("Helvetica", 12), date_pattern="mm-dd-yyyy", background="darkblue", foreground="white", borderwidth=2)
        self.fecha_inicio_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(options_frame, text="Fecha Fin:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=2, column=0, padx=10, pady=5)
        self.fecha_fin_entry = DateEntry(options_frame, width=12, font=("Helvetica", 12), date_pattern="mm-dd-yyyy", background="darkblue", foreground="white", borderwidth=2)
        self.fecha_fin_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botón para generar el reporte
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#2980b9",
            "fg": "white",
            "activebackground": "#3498db",
            "activeforeground": "white",
            "width": 15,
            "height": 1,
            "bd": 0,
            "relief": "solid"
        }
        tk.Button(self, text="Generar Reporte", command=self.generar_reporte, **button_style).pack(pady=10)

        # Tabla de reportes
        self.tree = ttk.Treeview(self, show="headings")
        self.tree.pack(pady=10, expand=True, fill="both")

    def generar_reporte(self):
        reporte_tipo = self.reporte_var.get()

        # Limpiar la tabla antes de cargar datos
        for i in self.tree.get_children():
            self.tree.delete(i)
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")

        if reporte_tipo == "Clientes":
            self.tree["columns"] = ("Clave", "Apellidos", "Nombres", "Teléfono")
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
            clients = get_all_clients()
            for client in clients:
                self.tree.insert("", tk.END, values=client)

        elif reporte_tipo == "Unidades":
            self.tree["columns"] = ("Clave", "Rodada", "Color")
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
            units = get_all_units()
            for unit in units:
                self.tree.insert("", tk.END, values=unit)

        elif reporte_tipo == "Retrasos":
            self.tree["columns"] = ("Unidad", "Rodada", "Color", "Cliente", "Fecha Préstamo", "Días Retraso")
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
            retrasos = get_retrasos()
            for retraso in retrasos:
                self.tree.insert("", tk.END, values=retraso)

        elif reporte_tipo == "Préstamos por Retornar (Período)" or reporte_tipo == "Préstamos por Período":
            fecha_inicio = self.fecha_inicio_entry.get()
            fecha_fin = self.fecha_fin_entry.get()

            # Validar las fechas ingresadas
            try:
                datetime.strptime(fecha_inicio, "%m-%d-%Y")
                datetime.strptime(fecha_fin, "%m-%d-%Y")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa las fechas en el formato mm-dd-aaaa.")
                return

            if reporte_tipo == "Préstamos por Retornar (Período)":
                self.tree["columns"] = ("Unidad", "Rodada", "Fecha Préstamo", "Cliente", "Teléfono")
                prestamos = get_prestamos_por_retornar(fecha_inicio, fecha_fin)
            else:
                self.tree["columns"] = ("Unidad", "Rodada", "Fecha Préstamo", "Cliente", "Teléfono")
                prestamos = get_prestamos_por_periodo(fecha_inicio, fecha_fin)

            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
            for prestamo in prestamos:
                self.tree.insert("", tk.END, values=prestamo)
