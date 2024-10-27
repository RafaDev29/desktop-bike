# views/unit_view.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controllers.unit_controller import add_unidad, get_unidades

class UnitView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Unidades")
        self.geometry("600x450")
        self.configure(bg="#f0f4f7")

        # Título de la ventana
        title_label = tk.Label(self, text="Gestión de Unidades", font=("Helvetica", 16, "bold"), bg="#f0f4f7", fg="#34495e")
        title_label.pack(pady=(10, 20))

        # Contenedor de formulario
        form_frame = tk.Frame(self, bg="#f0f4f7")
        form_frame.pack(pady=10)

        # Campos del formulario
        tk.Label(form_frame, text="Rodada:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.rodada_var = tk.IntVar()
        self.rodada_menu = ttk.Combobox(form_frame, textvariable=self.rodada_var, values=[20, 26, 29], state="readonly", font=("Helvetica", 12))
        self.rodada_menu.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Color:", font=("Helvetica", 12), bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.color_entry = tk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.color_entry.grid(row=1, column=1, padx=10, pady=5)

        # Botón para agregar unidad
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
        tk.Button(self, text="Agregar Unidad", command=self.add_unidad, **button_style).pack(pady=10)

        # Tabla para mostrar unidades
        self.tree = ttk.Treeview(self, columns=("Clave", "Rodada", "Color"), show="headings")
        self.tree.heading("Clave", text="Clave")
        self.tree.heading("Rodada", text="Rodada")
        self.tree.heading("Color", text="Color")
        self.tree.pack(pady=10)

        # Ajustes de estilos de la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 10))

        # Cargar lista de unidades
        self.load_unidades()

    def add_unidad(self):
        rodada = self.rodada_var.get()
        color = self.color_entry.get().strip()

        if not rodada or not color:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            add_unidad(rodada, color)
            messagebox.showinfo("Éxito", "Unidad agregada correctamente.")
            self.load_unidades()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        # Limpiar los campos de entrada
        self.rodada_menu.set("")
        self.color_entry.delete(0, tk.END)

    def load_unidades(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        unidades = get_unidades()
        for unidad in unidades:
            self.tree.insert("", tk.END, values=unidad)
