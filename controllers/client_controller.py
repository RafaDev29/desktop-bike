# controllers/client_controller.py
import sqlite3

def add_cliente(apellidos, nombres, telefono):
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()
    
    # Validar el formato del teléfono
    if len(telefono) != 10 or not telefono.isdigit():
        raise ValueError("El teléfono debe contener 9 dígitos")
    
    cursor.execute('''
    INSERT INTO Cliente (apellidos, nombres, telefono) 
    VALUES (?, ?, ?)
    ''', (apellidos, nombres, telefono))

    conn.commit()
    conn.close()

def get_clientes():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Cliente')
    clientes = cursor.fetchall()
    conn.close()

    return clientes
