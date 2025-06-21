import pandas as pd
from datetime import date
from latam_scraper import scrape
import matplotlib.pyplot as plt
import seaborn as sns

ano = 2023
input_path = f"data/clean/anac/resumo_anual_{ano}_filtrado.csv"

df = pd.read_csv(input_path, sep=';', encoding='utf-8')

df = df.dropna(subset=['PASSAGEIROS PAGOS', 'ASSENTOS', 'MÊS'])
df = df[df['ASSENTOS'] > 0]

agrupado = df.groupby(['AEROPORTO DE DESTINO (NOME)', 'MÊS'])[['PASSAGEIROS PAGOS', 'ASSENTOS']].sum().reset_index()

agrupado['TAXA OCUPAÇÃO (%)'] = (agrupado['PASSAGEIROS PAGOS'] / agrupado['ASSENTOS']) * 100

tabela_pivot = agrupado.pivot(index='AEROPORTO DE DESTINO (NOME)', columns='MÊS', values='TAXA OCUPAÇÃO (%)').fillna(0)

destinos_mais_movimentados = (
    df.groupby('AEROPORTO DE DESTINO (SIGLA)')['PASSAGEIROS PAGOS'].sum()
    .sort_values(ascending=False)
    .head(10)
)

icao_to_iata = {
    "SBAM": "MCP", "SWYN": "", "SNAL": "APQ", "SWBC": "BAZ", "SWBI": "", "SBBE": "BEL", "SBCF": "CNF", "SBBH": "PLU", "SBBV": "BVB", "SWBR": "", "SWBS": "", "SBBR": "BSB",
    "SBCD": "CFC", "SNCC": "", "SBKP": "VCP", "SDAM": "CPQ", "SBMT": "", "SNRU": "CAU", "SWCA": "CAF", "SBCA": "CAC", "SILQ": "", "SWKO": "CIZ", "SBAA": "CDJ", "SBCZ": "CZS",
    "SBBI": "BFH", "SBCT": "CWB", "SWFJ": "FEJ", "SWFN": "", "SBFL": "FLN", "SBFZ": "FOR", "SBFI": "IGU", "SBZM": "IZA", "SBGO": "GYN", "SBGR": "GRU", "SBIZ": "IMP", "SBJE": "JJD",
    "SBJV": "JOI", "SBJP": "JPA", "SBJF": "JDF", "SBJD": "QDV", "SBMQ": "MCP", "SBEG": "MAO", "SNML": "", "SBMO": "MCZ", "SBMS": "MVF", "SBNF": "NVT", "SBSG": "NAT",
    "SWNK": "", "SBOI": "", "SNOZ": "", "SWJV": "", "SBPB": "PHB", "SNPE": "", "SSZW": "PGZ", "SBPA": "POA", "SNPG": "", "SBPV": "PVH", "SBRF": "REC", "SBRP": "RAO",
    "SBRB": "RBR", "SBRJ": "SDU", "SBGL": "GIG", "SBJR": "", "SBRD": "ROO", "SBSM": "RIA", "SDOE": "", "SBST": "SSZ", "SBSV": "SSA", "SDSC": "QSC", "SBSL": "SLZ", "SBSP": "CGH",
    "SWSN": "ZMD", "SDCO": "SOD", "SWMU": "", "SBTT": "TBT", "SBTK": "TRQ", "SBTF": "TFF", "SBTE": "THE", "SBTS": "", "SNUN": "", "SWXU": "",
}

rotas = []
origem_padrao = "GYN"
for sigla_dest in destinos_mais_movimentados.index:
    dest_iata = icao_to_iata.get(sigla_dest)
    if dest_iata and dest_iata != origem_padrao:
        rotas.append((origem_padrao, dest_iata))

datas = [(date(2025, m, 15)).isoformat() for m in range(7, 13)]
for m in range(1, 6):
    datas.append(date(2026, m, 15).isoformat())

scrape(rotas, datas)

#destinos_mais_movimentados = (
#    df.groupby('AEROPORTO DE DESTINO (NOME)')['PASSAGEIROS PAGOS'].sum()
#    .sort_values(ascending=False)
#    .head(15)
#    .index
#)
#tabela_pivot = tabela_pivot.loc[destinos_mais_movimentados]
#
#plt.figure(figsize=(14, 8))
#sns.heatmap(tabela_pivot, cmap='YlGnBu', annot=True, fmt=".1f", linewidths=0.5, linecolor='gray')
#plt.title(f'Taxa de Ocupação (%) por Destino e Mês (Top 15 destinos) - Ano {ano}')
#plt.xlabel('Mês')
#plt.ylabel('Aeroporto de Destino')
#plt.tight_layout()
#plt.show()