#!/usr/bin/env python3
import sys
import time

def procesar_secuencial(filepath):
    start = time.time()
    resultados = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        next(f)  # Omitir encabezado
        for line in f:
            fields = line.strip().split(',')
            if len(fields) != 8:
                continue
            try:
                hora = fields[1].split(" ")[1].split(":")[0]
                cat = fields[3]
                ingreso = int(fields[5]) * float(fields[6])
                key = f"{hora}\t{cat}"
                resultados[key] = resultados.get(key, 0.0) + ingreso
            except ValueError:
                continue

    end = time.time()
    print(f"Tiempo Secuencial: {end - start:.2f} segundos")
    return resultados

if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "/data/input/ventas_125052199.csv"
    procesar_secuencial(archivo)