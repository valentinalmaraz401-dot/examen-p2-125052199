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

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                clave, valor = parts[0], float(parts[1])
                subclave = ""
            elif len(parts) == 3:
                clave, subclave, valor = parts[0], parts[1], float(parts[2])
            else:
                continue
            
            cur.execute(
                "INSERT INTO resultados (clave, subclave, valor) VALUES (%s, %s, %s);",
                (clave, subclave, valor)
            )

    conn.commit()
    print("Resultados cargados exitosamente a la base de datos.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    archivo_salida = sys.argv[1] if len(sys.argv) > 1 else "/app/mapreduce/salida/part-00000"
    cargar_datos(archivo_salida)