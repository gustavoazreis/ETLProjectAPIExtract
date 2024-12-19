import os
import time
import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, BitcoinPrice
from dotenv import load_dotenv

load_dotenv()
postgres_user = os.getenv("postgres_user")
postgres_password = os.getenv("postgres_password")
postgres_host = os.getenv("postgres_host")
postgres_port = os.getenv("postgres_port")
postgres_db = os.getenv("postgres_db")

database_url = (
    f"postgresql://{postgres_user}:{postgres_password}"
    f"@{postgres_host}:{postgres_port}/{postgres_db}"
)

engine = create_engine(database_url)
Session = sessionmaker(bind = engine)

def create_table():
    Base.metadata.create_all(engine)
    print("Tabela criada/verificada com sucesso!")

def extract_data_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na API: {response.status_code}")
        return None

def transform_data_bitcoin(dados):
    valor = float(dados["data"]["amount"])
    ativo = dados["data"]["base"]
    moeda = dados["data"]["currency"]
    timestamp = datetime.now()

    dados_transformados = {
        "valor": valor,
        "ativo": ativo,
        "moeda": moeda,
        "timestamp": timestamp
    }

    return dados_transformados

def load_data_postgres(dados):
    session = Session()
    novo_registro = BitcoinPrice(**dados)
    session.add(novo_registro)
    session.commit()
    session.close()
    print(f"[{dados['timestamp']}] Dados salvos no PostgreSQL")
    

if __name__ == "__main__":
    create_table()
    print("Iniciando ETL com atualização a cada 15 segundos...")

    while True:
        try:
            dados_json = extract_data_bitcoin()
            if dados_json:
                dados_tratados = transform_data_bitcoin(dados_json)
                print("Dados tratados:", dados_tratados)
                load_data_postgres(dados_tratados)
            time.sleep(15)
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo usuário. Finalizando...")
            break
        except Exception as e:
            print(f"Erro durante a execução: {e}")
            time.sleep(15)
