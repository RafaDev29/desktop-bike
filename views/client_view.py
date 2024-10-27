# views/client_view.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controllers.client_controller import add_cliente, get_clientes

class ClientView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Clientes")
        self.geometry("600x450")
        self.configure(bg="#f0f4f7")  # Fondo claro

        # Título de la ventana
        title_label = tk.Label(self, text="Gestión de Clientes", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#34495e")
        title_label.pack(pady=(10, 20))

        # Contenedor de formulario
        form_frame = tk.Frame(self, bg="#f0f4f7")
        form_frame.pack(pady=10)

        # Campos del formulario
        tk.Label(form_frame, text="Apellidos:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.apellidos_entry = tk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.apellidos_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Nombres:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.nombres_entry = tk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.nombres_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Teléfono:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.telefono_entry = tk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.telefono_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botón de agregar cliente
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
        tk.Button(self, text="Agregar Cliente", command=self.add_cliente, **button_style).pack(pady=10)

        # Tabla de clientes
        self.tree = ttk.Treeview(self, columns=("Clave", "Apellidos", "Nombres", "Teléfono"), show="headings")
        self.tree.heading("Clave", text="Clave")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Nombres", text="Nombres")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.pack(pady=10)

        # Ajustes de estilos de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 10))

        # Cargar lista de clientes
        self.load_clientes()

    def add_cliente(self):
        apellidos = self.apellidos_entry.get().strip()
        nombres = self.nombres_entry.get().strip()
        telefono = self.telefono_entry.get().strip()

        if not apellidos or not nombres or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            add_cliente(apellidos, nombres, telefono)
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            self.load_clientes()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        # Limpiar los campos de entrada
        self.apellidos_entry.delete(0, tk.END)
        self.nombres_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)

    def load_clientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        clientes = get_clientes()
        for cliente in clientes:
            self.tree.insert("", tk.END, values=cliente)
