#!/usr/bin/env python3
import os
import sys
import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "datamart")
DB_USER = os.getenv("DB_USER", "hadoop_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "hadoop_pass")
DB_PORT = os.getenv("DB_PORT", "5432")

def cargar_datos(filepath):
    if not os.path.exists(filepath):
        print(f"Error: No existe el archivo {filepath}")
        sys.exit(1)

    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE resultados;")

    registros = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()  # Maneja cualquier número de espacios/tabs
            if len(parts) >= 3:
                clave = parts[0]
                subclave = " ".join(parts[1:-1])
                try:
                    valor = float(parts[-1])
                    registros.append((clave, subclave, valor))
                except ValueError:
                    continue

    if registros:
        cur.executemany(
            "INSERT INTO resultados (clave, subclave, valor) VALUES (%s, %s, %s);",
            registros
        )

    conn.commit()
    print(f"Éxito: {len(registros)} resultados cargados a la base de datos.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    archivo_salida = sys.argv[1] if len(sys.argv) > 1 else "/app/mapreduce/salida/part-00000"
    cargar_datos(archivo_salida)