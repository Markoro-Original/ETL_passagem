import pandas as pd
import glob
import os

lista_arquivos = glob.glob("data/raw/latam/latam_*.csv")
arquivo_preco = max(lista_arquivos, key=os.path.getctime)

precos = pd.read_csv(arquivo_preco)
precos['data'] = pd.to_datetime(precos['data'])
precos['mes_ref'] = precos['data'].dt.to_period('M')
precos.rename(columns={'origem': 'origin', 'destino': 'dest'}, inplace=True)

df = pd.read_csv("data/raw/anac/filtrado/resumo_anual_2024_filtrado.csv", sep=';', encoding='utf-8')

df = df.dropna(subset=['PASSAGEIROS PAGOS', 'ASSENTOS', 'MÊS'])
df = df[df['ASSENTOS'] > 0]

agrupado = df.groupby(['AEROPORTO DE DESTINO (NOME)', 'MÊS'])[['PASSAGEIROS PAGOS', 'ASSENTOS']].sum().reset_index()

agrupado['TAXA OCUPAÇÃO (%)'] = (agrupado['PASSAGEIROS PAGOS'] / agrupado['ASSENTOS']) * 100

agrupado['mes_ref'] = pd.to_datetime(
    agrupado['MÊS'].astype(str) + '-2024', format='%m-%Y'
).dt.to_period("M")

icao_to_iata = {
    "SBAM": "MCP",
    "SWYN": "",
    "SNAL": "APQ",
    "SWBC": "BAZ",
    "SWBI": "",
    "SBBE": "BEL",
    "SBCF": "CNF",
    "SBBH": "PLU",
    "SBBV": "BVB",
    "SWBR": "",
    "SWBS": "",
    "SBBR": "BSB",
    "SBCD": "CFC",
    "SNCC": "",
    "SBKP": "VCP",
    "SDAM": "CPQ",
    "SBMT": "",
    "SNRU": "CAU",
    "SWCA": "CAF",
    "SBCA": "CAC",
    "SILQ": "",
    "SWKO": "CIZ",
    "SBAA": "CDJ",
    "SBCZ": "CZS",
    "SBBI": "BFH",
    "SBCT": "CWB",
    "SWFJ": "FEJ",
    "SWFN": "",
    "SBFL": "FLN",
    "SBFZ": "FOR",
    "SBFI": "IGU",
    "SBZM": "IZA",
    "SBGO": "GYN",
    "SBGR": "GRU",
    "SBIZ": "IMP",
    "SBJE": "JJD",
    "SBJV": "JOI",
    "SBJP": "JPA",
    "SBJF": "JDF",
    "SBJD": "QDV",
    "SBMQ": "MCP",
    "SBEG": "MAO",
    "SNML": "",
    "SBMO": "MCZ",
    "SBMS": "MVF",
    "SBNF": "NVT",
    "SBSG": "NAT",
    "SWNK": "",
    "SBOI": "",
    "SNOZ": "",
    "SWJV": "",
    "SBPB": "PHB",
    "SNPE": "",
    "SSZW": "PGZ",
    "SBPA": "POA",
    "SNPG": "",
    "SBPV": "PVH",
    "SBRF": "REC",
    "SBRP": "RAO",
    "SBRB": "RBR",
    "SBRJ": "SDU",
    "SBGL": "GIG",
    "SBJR": "",
    "SBRD": "ROO",
    "SBSM": "RIA",
    "SDOE": "",
    "SBST": "SSZ",
    "SBSV": "SSA",
    "SDSC": "QSC",
    "SBSL": "SLZ",
    "SBSP": "CGH",
    "SWSN": "ZMD",
    "SDCO": "SOD",
    "SWMU": "",
    "SBTT": "TBT",
    "SBTK": "TRQ",
    "SBTF": "TFF",
    "SBTE": "THE",
    "SBTS": "",
    "SNUN": "",
    "SWXU": "",
}

agrupado.rename(columns={'AEROPORTO DE DESTINO (SIGLA)': 'sigla_icao'}, inplace=True)
agrupado['dest'] = agrupado['sigla_icao'].map(icao_to_iata)

dados = pd.merge(
    precos,
    agrupado[['dest', 'mes_ref', 'TAXA OCUPAÇÃO (%)']],
    on=['dest', 'mes_ref'],
    how='left'
)
dados.rename(columns={'TAXA OCUPAÇÃO (%)': 'load_factor'}, inplace=True)

dados.to_parquet("data/clean/preco_load_merged.parquet", index=False)