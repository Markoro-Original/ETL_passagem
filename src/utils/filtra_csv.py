import pandas as pd

for ano in range(2000, 2026):
    input_path = f"data/raw/anac/resumo_anual_{ano}.csv"
    output_path = f"data/clean/anac/resumo_anual_{ano}_filtrado.csv"
    
    df = pd.read_csv(input_path, sep=';', encoding='ISO-8859-1')
    
    colunas_desejadas = [
        'EMPRESA (SIGLA)', 'EMPRESA (NOME)', 'ANO', 'MÊS',
        'AEROPORTO DE ORIGEM (SIGLA)', 'AEROPORTO DE ORIGEM (NOME)', 'AEROPORTO DE ORIGEM (UF)',
        'AEROPORTO DE DESTINO (SIGLA)', 'AEROPORTO DE DESTINO (NOME)', 'AEROPORTO DE DESTINO (UF)',
        'NATUREZA', 'GRUPO DE VOO', 'PASSAGEIROS PAGOS', 'PASSAGEIROS GRÁTIS', 'ASSENTOS'
    ]
    
    df_filtrado = df[
        (df['NATUREZA'] == 'DOMÉSTICA') &
        (df['GRUPO DE VOO'] == 'REGULAR')
    ]
    
    df_filtrado = df_filtrado[colunas_desejadas]
    
    #Trecho para remover casa decimal
    colunas_numericas = ['PASSAGEIROS PAGOS', 'PASSAGEIROS GRÁTIS', 'ASSENTOS']
    
    for col in colunas_numericas:
        df_filtrado[col] = pd.to_numeric(df_filtrado[col], errors='coerce')
        df_filtrado[col] = df_filtrado[col].dropna().astype('Int64')
    
    df_filtrado.to_csv(output_path, sep=';', index=False, encoding='utf-8')