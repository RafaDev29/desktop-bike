# views/loan_view.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controllers.loan_controller import add_prestamo, get_prestamos_activos
from controllers.client_controller import get_clientes
from controllers.unit_controller import get_unidades

class LoanView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Préstamos")
        self.geometry("800x500")
        self.configure(bg="#f0f4f7")

        title_label = tk.Label(self, text="Gestión de Préstamos", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#34495e")
        title_label.pack(pady=(10, 20))

        form_frame = tk.Frame(self, bg="#f0f4f7")
        form_frame.pack(pady=10)

        # Seleccionar cliente
        tk.Label(form_frame, text="Cliente:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.cliente_var = tk.StringVar()
        self.cliente_menu = ttk.Combobox(form_frame, textvariable=self.cliente_var, font=("Helvetica", 12))
        self.cliente_menu.grid(row=0, column=1, padx=10, pady=5)

        # Seleccionar unidad
        tk.Label(form_frame, text="Unidad:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.unidad_var = tk.StringVar()
        self.unidad_menu = ttk.Combobox(form_frame, textvariable=self.unidad_var, font=("Helvetica", 12))
        self.unidad_menu.grid(row=1, column=1, padx=10, pady=5)

        # Duración del préstamo
        tk.Label(form_frame, text="Días de Préstamo:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.dias_entry = tk.Entry(form_frame, width=5, font=("Helvetica", 12))
        self.dias_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Botón para registrar préstamo
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#2980b9",
            "fg": "white",
            "activebackground": "#3498db",
            "activeforeground": "white",
            "width": 20,
            "height": 1,
            "bd": 0,
            "relief": "solid"
        }
        tk.Button(self, text="Registrar Préstamo", command=self.add_prestamo, **button_style).pack(pady=10)

        # Tabla de préstamos activos
        self.tree = ttk.Treeview(self, columns=("Folio", "Clave Unidad", "Rodada", "Color", "Nombre Cliente", "Fecha Préstamo", "Días de Préstamo"), show="headings")
        
        # Ajustar encabezados de columnas
        for col in ("Folio", "Clave Unidad", "Rodada", "Color", "Nombre Cliente", "Fecha Préstamo", "Días de Préstamo"):
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # Estilos de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 10))

        # Cargar datos iniciales
        self.load_dropdowns()
        self.load_prestamos()

    def load_dropdowns(self):
        # Cargar clientes y unidades
        clientes = get_clientes()
        self.cliente_menu["values"] = [f"{c[0]} - {c[1]} {c[2]}" for c in clientes]

        unidades = get_unidades()
        self.unidad_menu["values"] = [f"{u[0]} - {u[1]} ({u[2]})" for u in unidades]

    def add_prestamo(self):
        try:
            clave_cliente = int(self.cliente_var.get().split(" - ")[0])
            clave_unidad = int(self.unidad_var.get().split(" - ")[0])
            dias_prestamo = int(self.dias_entry.get())

            add_prestamo(clave_unidad, clave_cliente, dias_prestamo)
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente.")
            self.load_prestamos()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        self.cliente_menu.set("")
        self.unidad_menu.set("")
        self.dias_entry.delete(0, tk.END)

    def load_prestamos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        prestamos = get_prestamos_activos()
        for prestamo in prestamos:
            self.tree.insert("", tk.END, values=prestamo)
