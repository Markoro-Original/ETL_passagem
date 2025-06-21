import requests
from bs4 import BeautifulSoup
import os
import urllib3
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://www.gov.br/anac/pt-br/assuntos/dados-e-estatisticas/dados-estatisticos/dados-estatisticos'


def criar_sessao():
    """Cria uma sessão com retry automático"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def extrair_links(url):
    session = criar_sessao()
    response = session.get(url, verify=False, timeout=30)
    if response.status_code != 200:
        print(f"Erro ao acessar página: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.endswith(('.xls', '.xlsx', '.csv', '.zip')):
            if not href.startswith('http'):
                href = 'https://www.gov.br' + href
            links.append(href)

    return links


def baixar_arquivos(links, pasta_destino='data/raw/anac'):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
    
    session = criar_sessao()
    
    for i, link in enumerate(links, 1):
        nome_arquivo = link.split('/')[-1]
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

        print(f"Baixando {nome_arquivo}... ({i}/{len(links)})")
        
        try:
            resposta = session.get(link, verify=False, timeout=60, stream=True)
            if resposta.status_code == 200:
                with open(caminho_arquivo, 'wb') as f:
                    for chunk in resposta.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Salvo em {caminho_arquivo}")
            else:
                print(f"Erro ao baixar {nome_arquivo}: {resposta.status_code}")
        except Exception as e:
            print(f"Erro ao baixar {nome_arquivo}: {str(e)}")
            # Remove arquivo parcial se existir
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
        
        # Pausa entre downloads para evitar sobrecarga
        if i < len(links):
            time.sleep(1)


links = extrair_links(url)
print(f"Total de arquivos encontrados: {len(links)}")
baixar_arquivos(links)
