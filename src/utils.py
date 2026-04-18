import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Anonimização de Dados
def anonimizar_dados(df: pd.DataFrame) -> pd.DataFrame:

    if not isinstance(df, pd.DataFrame) or df.empty:
        return df
        
    df_anon = df.copy()
    colunas_sensiveis = ['nome', 'nome_cliente', 'cliente', 'email', 'telefone']
    
    for col in df_anon.columns:
        if col.lower() in colunas_sensiveis:
            df_anon[col] = [f"Cliente_Anonimo_{i+1}" for i in range(len(df_anon))]
            
    return df_anon

# 2. Gerando Gráficos com Matplotlib
def gerar_grafico(df: pd.DataFrame, tipo_grafico: str, titulo: str = "Resultado da Análise"):

    if not isinstance(df, pd.DataFrame) or df.empty or len(df.columns) < 2:
        return "Dados insuficientes ou inválidos para gerar gráfico (necessário pelo menos 2 colunas)."

    col_x = df.columns[0]
    col_y = df.columns[1]
    
    df[col_x] = df[col_x].fillna("Sem Categoria").astype(str)
    
    plt.figure(figsize=(10, 6))
    
    try:
        if tipo_grafico.lower() == 'barras':
            plt.bar(df[col_x].astype(str), df[col_y], color='skyblue', edgecolor='black')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel(col_y)
            plt.xlabel(col_x)
            
        elif tipo_grafico.lower() == 'pizza':
            plt.pie(df[col_y], labels=df[col_x].astype(str), autopct='%1.1f%%', startangle=140)
            
        elif tipo_grafico.lower() == 'linha':
            plt.plot(df[col_x].astype(str), df[col_y], marker='o', color='green', linestyle='-')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel(col_y)
            plt.xlabel(col_x)
            plt.grid(True, linestyle='--', alpha=0.7)
            
        else:
            plt.close()
            return "Gráfico não recomendado ou tipo não suportado para esta query."
            
        plt.title(titulo)
        plt.tight_layout()
        
        caminho_arquivo = "grafico_analise.png"
        plt.savefig(caminho_arquivo)
        plt.close()
        
        return f"Gráfico gerado com sucesso e salvo como: {caminho_arquivo}"
        
    except Exception as e:
        plt.close()
        return f"Erro ao gerar o gráfico: {str(e)}"