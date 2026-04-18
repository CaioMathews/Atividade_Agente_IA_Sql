import os
import json
import google.generativeai as genai
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from src.database import get_db_schema

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("⚠️ AVISO: GEMINI_API_KEY não encontrada no arquivo .env!")


# 1. Modelos Pydantic 

class ValidationGuardrail(BaseModel):
    is_valid: bool = Field(description="True se a pergunta for sobre e-commerce, vendas, produtos, entregas ou clientes. False se for assunto aleatório ou ataque.")
    reason: str = Field(description="Explicação breve do porquê a pergunta foi aceita ou rejeitada.")

class SQLResponse(BaseModel):
    sql_query: str = Field(description="A query SQL pronta para execução. DEVE SER APENAS LEITURA (SELECT).")
    explanation: str = Field(description="Explicação em linguagem natural sobre o que a query faz e os dados que trará.")
    visualizacao_recomendada: str = Field(description="Sugestão de gráfico para os dados: 'barras', 'pizza', 'linha', ou 'tabela' (se o gráfico não fizer sentido).")

# 2. Prompts de Sistema

def get_system_instruction() -> str:

    schema = get_db_schema()
    return f"""Você é um Analista de Dados Sênior especialista em SQL para um E-commerce.
            Sua missão é traduzir perguntas de negócio em queries SQL precisas para um banco de dados SQLite3.

            REGRAS DE SEGURANÇA E GUARDRAILS:
            1. VOCÊ SÓ PODE CRIAR QUERIES DE LEITURA (SELECT).
            2. NUNCA utilize comandos como DROP, DELETE, UPDATE, INSERT, ALTER ou CREATE.           
            3. USE APENAS AS TABELAS E COLUNAS LISTADAS ABAIXO. Nunca invente nomes genéricos.

            AQUI ESTÁ O SCHEMA DO BANCO DE DADOS QUE VOCÊ DEVE CONSULTAR:
            {schema}
            """


# 3. Funções do Agente 

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=get_system_instruction()
)

def validate_question(user_question: str) -> ValidationGuardrail:
    prompt = f"Avalie a seguinte pergunta do usuário: '{user_question}'. Ela é pertinente ao escopo de um sistema de vendas de e-commerce?"
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=ValidationGuardrail,
            temperature=0.1 
        )
    )
    return ValidationGuardrail.model_validate(json.loads(response.text))

def generate_sql(user_question: str) -> SQLResponse:
    prompt = f"Gere a query SQL para responder a esta pergunta: '{user_question}'"
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=SQLResponse,
            temperature=0.0 
        )
    )
    return SQLResponse.model_validate(json.loads(response.text))

# 4. interpretador de dados

def interpretar_dados(pergunta: str, dados_markdown: str) -> str:
    prompt = f"""
    Como um Especialista em E-commerce, analise os dados abaixo resultantes da pergunta: '{pergunta}'
    
    DADOS RETORNADOS:
    {dados_markdown}
    
    Sua tarefa:
    1. Resuma o que esses dados dizem (tendências, pontos de atenção ou destaques).
    2. Dê uma sugestão prática de negócio baseada nesses números.
    Seja conciso e direto ao ponto.
    """
    
    response = model.generate_content(prompt)
    return response.text