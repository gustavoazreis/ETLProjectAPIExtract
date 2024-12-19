import time
import requests
from tinydb import TinyDB
from datetime import datetime

# Extração dos dados da API
def extract_data_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    dados = response.json()
    
    return dados

# Tranformação dos dados para tabela
def transform_data_bitcoin(dados):
    valor = dados["data"]["amount"]
    ativo = dados["data"]["base"]
    moeda = dados["data"]["currency"]
    timestamp = datetime.now().timestamp()

    dados_transformados = {
        "valor": valor,
        "ativo": ativo,
        "moeda": moeda,
        "timestamp": timestamp
    }

    return dados_transformados

# Carregamento dos dados no TinyDB
def load_data_tinydb(dados, db_name="bitcoin.json"):
    db = TinyDB(db_name)
    db.insert(dados)
    print("Dados salvos com sucesso.")

# Check de segurança + execução da pipeline
if __name__ == "__main__":
    while True:
        dados_json = extract_data_bitcoin()
        dados_tratados = transform_data_bitcoin(dados_json)
        load_data_tinydb(dados_tratados)
        time.sleep(15)