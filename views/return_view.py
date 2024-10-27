# views/return_view.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry  # Importar el widget de calendario
from controllers.return_controller import get_prestamos_pendientes, registrar_retorno
from datetime import datetime

class ReturnView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Retorno de Unidades")
        self.geometry("700x550")
        self.configure(bg="#f0f4f7")

        title_label = tk.Label(self, text="Retorno de Unidades", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#34495e")
        title_label.pack(pady=(10, 20))

        # Tabla de préstamos pendientes
        columns = ("Folio", "Clave Unidad", "Rodada", "Color", "Clave Cliente", "Nombre Cliente", "Fecha Préstamo", "Días de Préstamo")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        # Definir encabezados
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # Estilos de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 10))

        # Selección de fecha de retorno usando un calendario
        form_frame = tk.Frame(self, bg="#f0f4f7")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Fecha de Retorno:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.fecha_retorno_entry = DateEntry(form_frame, width=12, font=("Helvetica", 12), date_pattern="mm-dd-yyyy", background="darkblue", foreground="white", borderwidth=2)
        self.fecha_retorno_entry.grid(row=0, column=1, padx=10, pady=5)

        # Botón para registrar retorno
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
        tk.Button(self, text="Registrar Retorno", command=self.registrar_retorno, **button_style).pack(pady=10)

        # Cargar los préstamos pendientes
        self.load_prestamos_pendientes()

    def load_prestamos_pendientes(self):
        # Limpiar la tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Cargar datos en el orden correcto
        prestamos = get_prestamos_pendientes()
        for prestamo in prestamos:
            # Insertar datos en el orden correcto en la tabla
            self.tree.insert("", tk.END, values=prestamo)

    def registrar_retorno(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un préstamo para registrar el retorno.")
            return

        folio_prestamo = self.tree.item(selected_item)["values"][0]
        fecha_retorno = self.fecha_retorno_entry.get()

        # Validar y registrar la fecha de retorno
        try:
            datetime.strptime(fecha_retorno, "%m-%d-%Y")
            registrar_retorno(folio_prestamo, fecha_retorno)
            messagebox.showinfo("Éxito", "Retorno registrado correctamente.")
            self.load_prestamos_pendientes()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
