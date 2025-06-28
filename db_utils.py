import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def run_query(sql: str):
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
    conn.close()
    return columns, rows