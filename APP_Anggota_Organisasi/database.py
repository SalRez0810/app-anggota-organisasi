import sqlite3
import pandas as pd
from konfigurasi import DB_PATH

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"[DB ERROR] {e}")
        return None

def execute_query(query, params=()):
    conn = get_db_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"[QUERY ERROR] {e}")
        return None
    finally:
        conn.close()

def fetch_query(query, params=(), fetch_all=True):
    conn = get_db_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall() if fetch_all else cur.fetchone()
    finally:
        conn.close()

def get_dataframe(query, params=()):
    conn = get_db_connection()
    if not conn: return pd.DataFrame()
    try:
        return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        print(f"[DATAFRAME ERROR] {e}")
        return pd.DataFrame()
    finally:
        conn.close()