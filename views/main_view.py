# views/main_view.py
import tkinter as tk
from views.client_view import ClientView
from views.unit_view import UnitView
from views.loan_view import LoanView
from views.return_view import ReturnView
from views.report_view import ReportView  # Importar la vista de reportes
from views.analysis_view import AnalysisView  # Importa AnalysisView
class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Renta de Bicicletas")
        self.geometry("600x400")
        self.configure(bg="#f0f4f7")

        title_label = tk.Label(self, text="Sistema de Renta de Bicicletas", font=("Helvetica", 18, "bold"), bg="#f0f4f7", fg="#34495e")
        title_label.pack(pady=(20, 20))

        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#2980b9",
            "fg": "white",
            "activebackground": "#3498db",
            "activeforeground": "white",
            "width": 20,
            "height": 2,
            "bd": 0,
            "relief": "solid"
        }

        tk.Button(self, text="Gestión de Clientes", command=self.open_client_view, **button_style).pack(pady=(10, 10))
        tk.Button(self, text="Gestión de Unidades", command=self.open_unit_view, **button_style).pack(pady=(10, 10))
        tk.Button(self, text="Gestión de Préstamos", command=self.open_loan_view, **button_style).pack(pady=(10, 10))
        tk.Button(self, text="Registro de Retorno", command=self.open_return_view, **button_style).pack(pady=(10, 10))
        tk.Button(self, text="Informes y Reportes", command=self.open_report_view, **button_style).pack(pady=(10, 10))
        tk.Button(self, text="Análisis Descriptivo", command=self.open_analysis_view, **button_style).pack(pady=(10, 10))
    def open_client_view(self):
        client_view = ClientView(self)
        client_view.grab_set()

    def open_unit_view(self):
        unit_view = UnitView(self)
        unit_view.grab_set()

    def open_loan_view(self):
        loan_view = LoanView(self)
        loan_view.grab_set()

    def open_return_view(self):
        return_view = ReturnView(self)
        return_view.grab_set()

    def open_report_view(self):
        report_view = ReportView(self)
        report_view.grab_set()
        
    def open_analysis_view(self):
        analysis_view = AnalysisView(self)
        analysis_view.grab_set()
