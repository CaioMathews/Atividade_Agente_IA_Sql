# 🚀 Agente Analista de E-commerce (Text-to-SQL)

Este projeto é um Agente de Inteligência Artificial capaz de transformar perguntas de negócio em linguagem natural em consultas SQL precisas, executá-las em um banco de dados de E-commerce e retornar insights estratégicos, gráficos e dados protegidos.

## 🛠️ Funcionalidades Principais

* **Text-to-SQL Dinâmico:** Converte perguntas como "Quem são meus melhores clientes?" em queries SQL.
* **Guardrails de Segurança:** Validação via Pydantic que impede perguntas fora de escopo ou comandos maliciosos (`DROP`, `DELETE`).
* **Anonimização LGPD:** Filtro automático que mascara nomes e dados sensíveis dos clientes antes de exibir os resultados.
* **Visualização de Dados:** Geração automática de gráficos (barras, pizza, linhas) baseada na recomendação do Agente.
* **Análise de Especialista:** O agente não apenas entrega os dados, mas atua como um Cientista de Dados, interpretando os resultados e sugerindo ações de negócio.

## 📁 Estrutura do Projeto

```text
├── data/
│   └── banco.db           # Banco de dados SQLite de E-commerce
├── src/
│   ├── __init__.py
│   ├── agent.py           # Cérebro do agente (Gemini + Pydantic)
│   ├── database.py        # Camada de conexão e extração de Schema
│   └── utils.py           # Funções de Gráficos e Anonimização
├── main.py                # Ponto de entrada (Interface do Usuário)
├── .env                   # Chave da API (Não enviada ao Git)
├── .gitignore             # Proteção de arquivos sensíveis
└── requirements.txt       # Dependências do projeto

```
# 🚀 Como Executar

 

**1. Crie e ative um ambiente virtual**

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

**2. Configurar o Ambiente Virtual**

```bash
python -m venv venv

# No Windows:

venv\Scripts\activate

# No Mac/Linux:

source venv/bin/activate
```

**3. Instalar Dependências**

```bash
pip install -r requirements.txt
```

**4. Configurar Variáveis de Ambiente**

Crie um arquivo .env (seguindo o exemplo do arquivo .env.example) na raiz do projeto e adicione sua chave do Google Gemini:

```bash
GEMINI_API_KEY=sua_chave_aqui
```

**5. Instalar Dependências**

Crie uma pasta chamada data na raiz do projeto e coloque o arquivo banco.db dentro dela.

**6. Rodar o Agente**

```bash
python main.py
```