import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'banco.db')

def get_db_connection():

    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def execute_read_query(query: str):

    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            conn.close()
            return f"Erro na execução da query: {str(e)}"
    return "Falha na conexão com o banco."

def get_db_schema():

    conn = get_db_connection()
    schema_text = ""
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_text = "\n\n".join([table[0] for table in tables if table[0]])
        conn.close()
        
    return schema_text

def get_table_sample(table_name: str, limit: int = 5):

    query = f"SELECT * FROM {table_name} LIMIT {limit};"
    
    df = execute_read_query(query)
    
    if isinstance(df, pd.DataFrame) and not df.empty:
        return df.to_markdown(index=False)
    
    return f"Nenhum dado encontrado para a tabela {table_name}."