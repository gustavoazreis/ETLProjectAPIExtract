import os
import time
import requests
import logging
import logfire
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from logging import basicConfig, getLogger
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# Importando infos do database.py
from database import Base, BitcoinPrice

# Configuração do logfire
logfire.configure()
basicConfig(handlers = [logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()
logfire.instrument_sqlalchemy()

# Carregando e lendo as variáveis de ambiente do .env
load_dotenv()
postgres_user = os.getenv("postgres_user")
postgres_password = os.getenv("postgres_password")
postgres_host = os.getenv("postgres_host")
postgres_port = os.getenv("postgres_port")
postgres_db = os.getenv("postgres_db")

# Montando a URL de conexão ao PostgreSQL
database_url = (
    f"postgresql://{postgres_user}:{postgres_password}"
    f"@{postgres_host}:{postgres_port}/{postgres_db}"
)

# Cria o engine e a sessão
engine = create_engine(database_url)
Session = sessionmaker(bind = engine)

# Criação da tabela
def create_table():
    Base.metadata.create_all(engine)
    logger.info("Tabela criada/verificada com sucesso!")

# Extração dos dados da API
def extract_data_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na API: {response.status_code}")
        return None

# Tranformação dos dados para tabela
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

# Carregamento dos dados no PostgreSQL
def load_data_postgres(dados):
    session = Session()
    try:
        novo_registro = BitcoinPrice(**dados)
        session.add(novo_registro)
        session.commit()
        session.close()
    except Exception as ex:
        logger.error(f"Erro ao inserir dados no PostgreSQL: {ex}")
        session.rollback()
    finally:
        session.close()

# Execução da pipeline
def pipeline_bitcoin():
    with logfire.span("Executando pipeline ETL Bitcoin"):
        with logfire.span("Extrair Dados da API Coinbase"):
            dados_json = extract_data_bitcoin()
        if not dados_json:
            logger.error("Falha na extração dos dados. Abortando pipeline.")
            return
        with logfire.span("Tratar dados do Bitcoin"):
            dados_tratados = transform_data_bitcoin(dados_json)
        with logfire.span("Salvar dados no PostgreSQL"):
            load_data_postgres(dados_tratados)
        logger.info(f"Pipeline finalizada com sucesso!")

# Web server simples para o erro de Port
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"A execucao do ETL esta funcionando")

def start_web_server():
    port = int(os.getenv("PORT", 8000)) #porta coringa do Render
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    logger.info(f"Web server running on port {port}")
    server.serve_forever()


# Check de segurança
if __name__ == "__main__":
    create_table()
    logger.info("Iniciando pipeline ETL com atualização a cada 15 segundos...")

    # Inicia o server
    web_server_thread = Thread(target = start_web_server, daemon = True)
    web_server_thread.start()

    while True:
        try:
            pipeline_bitcoin()
            time.sleep(15)
        except KeyboardInterrupt:
            logger.info("Processo interrompido pelo usuário. Finalizando...")
            break
        except Exception as e:
            logger.info(f"Erro durante a pipeline: {e}")
            time.sleep(15)
