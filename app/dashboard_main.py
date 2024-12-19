import streamlit as st
import psycopg2
import pandas as pd
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Carregando e lendo as variáveis de ambiente do .env
load_dotenv()
postgres_user = os.getenv("postgres_user")
postgres_password = os.getenv("postgres_password")
postgres_host = os.getenv("postgres_host")
postgres_port = os.getenv("postgres_port")
postgres_db = os.getenv("postgres_db")

# Query dos dados necessários - no PostgreSQL - para o dashboard
def read_data_postgres():
    try:
        conn = psycopg2.connect(
            host = postgres_host,
            database = postgres_db,
            user = postgres_user,
            password = postgres_password,
            port = postgres_port
        )
        query = "SELECT * FROM bitcoin_price ORDER BY timestamp DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar ao PostgreSQL: {e}")
        return pd.DataFrame()

# Dashboard
def main():
    st.set_page_config(page_title="Dashboard de Preços do Bitcoin", layout="wide")
    st.title("📊 Dashboard de Preços do Bitcoin")
    st.write("Este dashboard exibe os dados do preço do Bitcoin coletados periodicamente em um banco PostgreSQL.")

    df = read_data_postgres()

    if not df.empty:
        st.subheader("📋 Dados Recentes")
        st.dataframe(df)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')
        
        st.subheader("📈 Evolução do Preço do Bitcoin")
        st.line_chart(data=df, x='timestamp', y='valor', use_container_width=True)

        st.subheader("🔢 Estatísticas Gerais")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Atual", f"${df['valor'].iloc[-1]:,.2f}")
        col2.metric("Preço Máximo", f"${df['valor'].max():,.2f}")
        col3.metric("Preço Mínimo", f"${df['valor'].min():,.2f}")
    else:
        st.warning("Nenhum dado encontrado no banco de dados PostgreSQL.")

if __name__ == "__main__":
    main()