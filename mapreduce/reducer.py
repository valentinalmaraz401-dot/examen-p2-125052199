#!/usr/bin/env python3
import sys

current_key = None
total_ingreso = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 3:
        continue
    
    hora, cat, ingreso_str = parts
    key = f"{hora}\t{cat}"
    
    try:
        ingreso = float(ingreso_str)
    except ValueError:
        continue

    if current_key == key:
        total_ingreso += ingreso
    else:
        if current_key:
            h, c = current_key.split("\t")
            print(f"{h}\t{c}\t{total_ingreso:.2f}")
        current_key = key
        total_ingreso = ingreso

if current_key:
    h, c = current_key.split("\t")
    print(f"{h}\t{c}\t{total_ingreso:.2f}")