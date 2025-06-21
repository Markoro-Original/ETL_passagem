import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_parquet("data/clean/merged/preco_load_merged.parquet")

df.rename(columns={'menor preço': 'preco'}, inplace=True)
df = df.dropna(subset=['preco', 'data', 'dest'])
df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
df = df[df['preco'] > 0]
df['data'] = pd.to_datetime(df['data'])
menor_preco_diario = df.groupby(['data', 'dest'])['preco'].min().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=menor_preco_diario, x='data', y='preco', hue='dest', marker='o')

plt.title("Evolução do menor preço LATAM por destino")
plt.xlabel("Data do voo")
plt.ylabel("Menor preço (R$)")
plt.grid(True, linestyle='--', alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend(title="Destino")
plt.show()