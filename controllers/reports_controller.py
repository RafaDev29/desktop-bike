# controllers/reports_controller.py
import sqlite3
from datetime import datetime
import pandas as pd
from scipy import stats
import numpy as np

def get_all_clients():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    cursor.execute("SELECT clave, apellidos, nombres, telefono FROM Cliente")
    clients = cursor.fetchall()
    conn.close()
    return clients

def get_all_units():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    cursor.execute("SELECT clave, rodada, color FROM Unidad")
    units = cursor.fetchall()
    conn.close()
    return units
def get_retrasos():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    # Calcular días de retraso y filtrar los registros con retraso usando WHERE
    cursor.execute('''
    SELECT Unidad.clave AS unidad, 
           Unidad.rodada, 
           Unidad.color, 
           Cliente.nombres || ' ' || Cliente.apellidos AS nombre_cliente, 
           Prestamo.fecha_prestamo, 
           (julianday('now') - julianday(Prestamo.fecha_prestamo)) - Prestamo.dias_prestamo AS dias_retraso
    FROM Prestamo
    JOIN Unidad ON Prestamo.clave_unidad = Unidad.clave
    JOIN Cliente ON Prestamo.clave_cliente = Cliente.clave
    WHERE Prestamo.fecha_retorno IS NULL AND dias_retraso > 0
    ORDER BY dias_retraso DESC
    ''')

    retrasos = cursor.fetchall()
    conn.close()
    return retrasos
def get_prestamos_por_retornar(fecha_inicio, fecha_fin):
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT Unidad.clave, Unidad.rodada, Prestamo.fecha_prestamo, Cliente.nombres || ' ' || Cliente.apellidos AS cliente, Cliente.telefono
    FROM Prestamo
    JOIN Unidad ON Prestamo.clave_unidad = Unidad.clave
    JOIN Cliente ON Prestamo.clave_cliente = Cliente.clave
    WHERE Prestamo.fecha_retorno IS NULL AND Prestamo.fecha_prestamo BETWEEN ? AND ?
    ORDER BY Prestamo.fecha_prestamo
    ''', (fecha_inicio, fecha_fin))

    prestamos = cursor.fetchall()
    conn.close()
    return prestamos

def get_prestamos_por_periodo(fecha_inicio, fecha_fin):
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT Unidad.clave, Unidad.rodada, Prestamo.fecha_prestamo, Cliente.nombres || ' ' || Cliente.apellidos AS cliente, Cliente.telefono
    FROM Prestamo
    JOIN Unidad ON Prestamo.clave_unidad = Unidad.clave
    JOIN Cliente ON Prestamo.clave_cliente = Cliente.clave
    WHERE Prestamo.fecha_prestamo BETWEEN ? AND ?
    ORDER BY Prestamo.fecha_prestamo
    ''', (fecha_inicio, fecha_fin))

    prestamos = cursor.fetchall()
    conn.close()
    return prestamos
def get_duracion_prestamos():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT dias_prestamo FROM Prestamo')
    duraciones = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not duraciones:
        return None

    # Calcular estadísticas descriptivas
    moda_result = stats.mode(duraciones)
    # Revisar si moda_result es un arreglo o un valor único
    moda = moda_result.mode[0] if isinstance(moda_result.mode, np.ndarray) else moda_result.mode

    return {
        'media': np.mean(duraciones),
        'mediana': np.median(duraciones),
        'moda': moda,
        'minimo': np.min(duraciones),
        'maximo': np.max(duraciones),
        'desviacion': np.std(duraciones),
        'cuartiles': np.percentile(duraciones, [25, 50, 75])
    }


def get_ranking_clientes():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT Cliente.clave, Cliente.nombres || ' ' || Cliente.apellidos AS nombre, Cliente.telefono, COUNT(*) AS cantidad_prestamos
    FROM Prestamo
    JOIN Cliente ON Prestamo.clave_cliente = Cliente.clave
    GROUP BY Cliente.clave
    ORDER BY cantidad_prestamos DESC
    ''')
    
    ranking = cursor.fetchall()
    conn.close()
    
    return ranking

def get_preferencias_por_rodada():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT Unidad.rodada, COUNT(*) AS cantidad_prestamos
    FROM Prestamo
    JOIN Unidad ON Prestamo.clave_unidad = Unidad.clave
    GROUP BY Unidad.rodada
    ORDER BY cantidad_prestamos DESC
    ''')
    
    preferencias = cursor.fetchall()
    conn.close()
    
    return preferencias

def get_preferencias_por_color():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT Unidad.color, COUNT(*) AS cantidad_prestamos
    FROM Prestamo
    JOIN Unidad ON Prestamo.clave_unidad = Unidad.clave
    GROUP BY Unidad.color
    ORDER BY cantidad_prestamos DESC
    ''')
    
    preferencias = cursor.fetchall()
    conn.close()
    
    return preferencias

def get_preferencias_por_dia():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()

    # Convertir fecha de mm-dd-yyyy a yyyy-mm-dd y luego extraer el día de la semana
    cursor.execute('''
    SELECT strftime('%w', substr(fecha_prestamo, 7, 4) || '-' || substr(fecha_prestamo, 1, 2) || '-' || substr(fecha_prestamo, 4, 2)) AS dia_semana, 
           COUNT(*) AS cantidad_prestamos
    FROM Prestamo
    WHERE fecha_prestamo IS NOT NULL
    GROUP BY dia_semana
    ORDER BY dia_semana
    ''')

    dias = {
        "0": "Domingo", "1": "Lunes", "2": "Martes", "3": "Miércoles",
        "4": "Jueves", "5": "Viernes", "6": "Sábado"
    }

    preferencias = [(dias.get(str(row[0]), "Día desconocido"), row[1]) for row in cursor.fetchall()]
    conn.close()

    return preferencias