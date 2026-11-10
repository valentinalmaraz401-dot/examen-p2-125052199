#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("id,"):
        continue
    fields = line.split(",")
    if len(fields) != 8:
        continue
    try:
        fecha_hora = fields[1]
        hora = fecha_hora.split(" ")[1].split(":")[0]  # Extrae HH (00-23)
        categoria = fields[3]
        ingreso = int(fields[5]) * float(fields[6])
        print(f"{hora}\t{categoria}\t{ingreso:.2f}")
    except ValueError:
        continue