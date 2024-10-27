# database/db_setup.py
import sqlite3

def create_tables():
    conn = sqlite3.connect('database/bike_rental.db')
    cursor = conn.cursor()
    
    # Tabla de Unidades
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Unidad (
        clave INTEGER PRIMARY KEY AUTOINCREMENT,
        rodada INTEGER NOT NULL CHECK (rodada IN (20, 26, 29)),
        color TEXT NOT NULL CHECK (length(color) <= 15)
    )
    ''')

    # Tabla de Clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cliente (
        clave INTEGER PRIMARY KEY AUTOINCREMENT,
        apellidos TEXT NOT NULL CHECK (length(apellidos) <= 40),
        nombres TEXT NOT NULL CHECK (length(nombres) <= 40),
        telefono TEXT NOT NULL CHECK (length(telefono) = 10 AND telefono GLOB '[0-9]*')
    )
    ''')

    # Tabla de Préstamos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prestamo (
        folio INTEGER PRIMARY KEY AUTOINCREMENT,
        clave_unidad INTEGER NOT NULL,
        clave_cliente INTEGER NOT NULL,
        fecha_prestamo TEXT NOT NULL,
        dias_prestamo INTEGER NOT NULL CHECK (dias_prestamo BETWEEN 1 AND 14),
        fecha_retorno TEXT,
        FOREIGN KEY (clave_unidad) REFERENCES Unidad(clave),
        FOREIGN KEY (clave_cliente) REFERENCES Cliente(clave)
    )
    ''')

    # Cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
