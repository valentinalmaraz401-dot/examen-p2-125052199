from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI(title="DataMart Analytics API")

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "datamart")
DB_USER = os.getenv("DB_USER", "hadoop_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "hadoop_pass")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )

class RegistroResultado(BaseModel):
    clave: str
    subclave: str = ""
    valor: float

@app.on_event("startup")
def setup_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id SERIAL PRIMARY KEY,
            clave VARCHAR(255) NOT NULL,
            subclave VARCHAR(255),
            valor NUMERIC(14,2) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.get("/resultados")
def get_all_resultados():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT clave, subclave, valor FROM resultados;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"clave": r[0], "subclave": r[1], "valor": float(r[2])} for r in rows]

@app.get("/resultados/{clave}")
def get_resultado_by_clave(clave: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT clave, subclave, valor FROM resultados WHERE clave = %s;", (clave,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Clave no encontrada")
    return [{"clave": r[0], "subclave": r[1], "valor": float(r[2])} for r in rows]

@app.post("/resultados", status_code=201)
def create_resultado(item: RegistroResultado):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO resultados (clave, subclave, valor) VALUES (%s, %s, %s) RETURNING id;",
        (item.clave, item.subclave, item.valor)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Creado exitosamente", "id": new_id, "item": item}