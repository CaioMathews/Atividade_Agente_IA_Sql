from src.agent import interpretar_dados, validate_question, generate_sql
from src.database import execute_read_query
from src.utils import anonimizar_dados, gerar_grafico
import pandas as pd

pd.options.display.float_format = '{:.2f}'.format

def executar_agente():

    print("🚀 Bem-vindo ao Agente Analista de E-commerce!")
    print("Digite 'sair' para encerrar.\n")
    
    while True:
        user_input = input("👤 Você: ")
        
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando o agente. Até logo!")
            break
            
        print("\n⏳ Agente processando...")
        
        validacao = validate_question(user_input)

        if not validacao.is_valid:
            print(f"🛑 Consulta Bloqueada: {validacao.reason}\n")
            continue
            
        try:
            resposta_agente = generate_sql(user_input)
            print(f"🧠 Explicação: {resposta_agente.explanation}")
            print(f"💻 SQL Gerado: \n{resposta_agente.sql_query}\n")
            
            df_resultado = execute_read_query(resposta_agente.sql_query)
            
            if isinstance(df_resultado, str): 
                print(f"❌ Erro no banco: {df_resultado}\n")
                continue
                
            if df_resultado.empty:
                print("📊 Resultado: A query não retornou nenhum dado.\n")
                continue
                
            df_seguro = anonimizar_dados(df_resultado)
            
            print("📊 Resultado da Consulta:")
            print(df_seguro.to_markdown(index=False))
            print("\n")

            print("🧐 Análise do Especialista:")
            insight = interpretar_dados(user_input, df_seguro.to_markdown(index=False))
            print(f"{insight}\n")
            
            sugestao_grafico = resposta_agente.visualizacao_recomendada

            if sugestao_grafico.lower() != 'tabela':
                print(f"📈 Tentando gerar gráfico do tipo: {sugestao_grafico}")
                status_grafico = gerar_grafico(df_seguro, sugestao_grafico)
                print(f"🖼️ Status: {status_grafico}\n")
                
        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado: {e}\n")

if __name__ == "__main__":
    executar_agente()