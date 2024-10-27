# controllers/unit_controller.py
import sqlite3

def add_unidad(rodada, color):
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    # Validación básica de rodada y color
    if rodada not in [20, 26, 29]:
        raise ValueError("La rodada debe ser 20, 26 o 29.")
    if len(color) > 15:
        raise ValueError("El color no puede tener más de 15 caracteres.")

    cursor.execute('''
    INSERT INTO Unidad (rodada, color) 
    VALUES (?, ?)
    ''', (rodada, color))

    conn.commit()
    conn.close()

def get_unidades():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Unidad')
    unidades = cursor.fetchall()
    conn.close()

    return unidades
