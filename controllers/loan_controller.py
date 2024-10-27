# controllers/loan_controller.py
import sqlite3
from datetime import datetime, timedelta

def add_prestamo(clave_unidad, clave_cliente, dias_prestamo, fecha_prestamo=None):
    # Si la fecha no se proporciona, usamos la fecha actual
    if not fecha_prestamo:
        fecha_prestamo = datetime.now().strftime("%m-%d-%Y")
    
    # Validación de días de préstamo
    if dias_prestamo < 1 or dias_prestamo > 14:
        raise ValueError("La duración del préstamo debe ser entre 1 y 14 días.")
    
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    # Asegurarse de que la unidad esté disponible (no prestada)
    cursor.execute("SELECT * FROM Prestamo WHERE clave_unidad = ? AND fecha_retorno IS NULL", (clave_unidad,))
    unidad_prestada = cursor.fetchone()
    if unidad_prestada:
        raise ValueError("La unidad seleccionada ya está prestada.")

    # Insertar el nuevo préstamo
    cursor.execute('''
    INSERT INTO Prestamo (clave_unidad, clave_cliente, fecha_prestamo, dias_prestamo)
    VALUES (?, ?, ?, ?)
    ''', (clave_unidad, clave_cliente, fecha_prestamo, dias_prestamo))

    conn.commit()
    conn.close()

def get_prestamos_activos():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    # Consultar préstamos donde la fecha de retorno es NULL (es decir, aún no retornados)
    cursor.execute('''
    SELECT Prestamo.folio, 
           Unidad.clave AS clave_unidad, 
           Unidad.rodada, 
           Unidad.color, 
           Cliente.nombres || ' ' || Cliente.apellidos AS nombre_cliente,  -- Nombre completo del cliente
           Prestamo.fecha_prestamo, 
           Prestamo.dias_prestamo
    FROM Prestamo
    JOIN Unidad ON Prestamo.clave_unidad = Unidad.clave
    JOIN Cliente ON Prestamo.clave_cliente = Cliente.clave
    WHERE Prestamo.fecha_retorno IS NULL
    ORDER BY Prestamo.fecha_prestamo DESC
    ''')

    prestamos = cursor.fetchall()
    conn.close()
    
    return prestamos
