import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

REALM = os.getenv("REALM")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
AGENT_ID = "01K6101856EC0MKJ8KN4S2B9CM"  # fixo do seu exemplo

# Função para autenticação
def get_jwt():
    token_url = f"https://idm.stackspot.com/{REALM}/oidc/oauth/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_KEY
    }
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_response.raise_for_status()
    return token_response.json()["access_token"]

# Função para chamar o agente
def ask_agent(prompt):
    jwt = get_jwt()
    agent_url = f"https://genai-inference-app.stackspot.com/v1/agent/{AGENT_ID}/chat"
    payload = {
        "streaming": False,
        "user_prompt": prompt,
        "stackspot_knowledge": False,
        "return_ks_in_response": True
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
    response = requests.post(agent_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Interface Streamlit
st.set_page_config(page_title="Gerador de Plano de Negócios", page_icon="📊", layout="centered")

st.title("📊 Gerador de Mini Plano de Negócios")
st.write("Digite sua ideia de negócio abaixo e receba um mini plano automaticamente.")

prompt = st.text_area("💡 Sua ideia de negócio:")

if st.button("Gerar Plano"):
    if prompt.strip():
        with st.spinner("Gerando plano de negócio..."):
            try:
                result = ask_agent(prompt)
                st.subheader("📑 Resultado")
                # Exibe texto formatado se possível
                if "text" in result:
                    st.write(result["text"])
                else:
                    st.json(result)  # fallback se a resposta vier em JSON diferente
            except Exception as e:
                st.error(f"Erro ao gerar plano: {e}")
    else:
        st.warning("Por favor, escreva uma ideia antes de gerar o plano.")
