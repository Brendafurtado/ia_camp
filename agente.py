import os
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env, se existir
load_dotenv()

# Pegue as variáveis de ambiente
REALM = os.getenv("REALM")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
AGENT_ID = "01K6101856EC0MKJ8KN4S2B9CM"  # Fixo conforme seu exemplo

# 1. Autenticação para obter o JWT
token_url = f"https://idm.stackspot.com/{REALM}/oidc/oauth/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_KEY
}
token_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
token_response = requests.post(token_url, data=token_data, headers=token_headers)
token_response.raise_for_status()
jwt = token_response.json()["access_token"]

# 2. Envio do prompt para o agente
agent_url = f"https://genai-inference-app.stackspot.com/v1/agent/{AGENT_ID}/chat"
payload = {
    "streaming": True,
    "user_prompt": "Descreva sua ideia de negócio para receber um mini plano de negócios. Exemplo: 'Quero abrir uma lanchonete vegana'.",  # Coloque sua pergunta aqui!
    "stackspot_knowledge": False,
    "return_ks_in_response": True
}
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt}"
}
response = requests.post(agent_url, json=payload, headers=headers)
print(response.text)