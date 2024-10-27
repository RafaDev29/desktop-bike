# controllers/return_controller.py
import sqlite3
from datetime import datetime

def get_prestamos_pendientes():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    # Consulta que obtiene los datos en el orden de columnas de ReturnView
    cursor.execute('''
    SELECT Prestamo.folio, 
           Unidad.clave AS clave_unidad, 
           Unidad.rodada, 
           Unidad.color, 
           Cliente.clave AS clave_cliente, 
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
def registrar_retorno(folio_prestamo, fecha_retorno):
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    # Validación de fecha de retorno no anterior a la fecha del préstamo
    cursor.execute("SELECT fecha_prestamo FROM Prestamo WHERE folio = ?", (folio_prestamo,))
    fecha_prestamo = cursor.fetchone()[0]

    if datetime.strptime(fecha_retorno, "%m-%d-%Y") < datetime.strptime(fecha_prestamo, "%m-%d-%Y"):
        raise ValueError("La fecha de retorno no puede ser anterior a la fecha del préstamo.")

    # Actualizar la fecha de retorno en el préstamo
    cursor.execute('''
    UPDATE Prestamo
    SET fecha_retorno = ?
    WHERE folio = ?
    ''', (fecha_retorno, folio_prestamo))

    conn.commit()
    conn.close()
