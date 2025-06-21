import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carrega e prepara os dados ANAC
df_anac = pd.read_csv("data/clean/anac/resumo_anual_2023_filtrado.csv", sep=";", encoding="utf-8")

# Remove linhas incompletas
df_anac = df_anac.dropna(subset=['PASSAGEIROS PAGOS', 'MÊS', 'AEROPORTO DE DESTINO (SIGLA)'])

# Garante que a coluna MÊS seja numérica
df_anac['MÊS'] = pd.to_numeric(df_anac['MÊS'], errors='coerce')

# Identifica os 3 destinos mais movimentados em número de passageiros
top_destinos = (
    df_anac.groupby('AEROPORTO DE DESTINO (SIGLA)')['PASSAGEIROS PAGOS']
    .sum()
    .sort_values(ascending=False)
    .head(3)
    .index
)

# Filtra apenas os dados desses 3 destinos
df_top = df_anac[df_anac['AEROPORTO DE DESTINO (SIGLA)'].isin(top_destinos)].copy()

# Cria coluna de data para plotagem
df_top['data'] = pd.to_datetime(df_top['MÊS'].astype(int).astype(str) + '-2023', format='%m-%Y')

# Agrupa por mês e destino
df_plot = df_top.groupby(['data', 'AEROPORTO DE DESTINO (SIGLA)'])['PASSAGEIROS PAGOS'].sum().reset_index()

# Gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_plot, x='data', y='PASSAGEIROS PAGOS', hue='AEROPORTO DE DESTINO (SIGLA)', marker='o')

plt.title("Evolução de passageiros pagos nos 3 destinos mais movimentados (2023)")
plt.xlabel("Mês")
plt.ylabel("Passageiros pagos")
plt.grid(True, linestyle='--', alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend(title="Destino (ICAO)")
plt.show()