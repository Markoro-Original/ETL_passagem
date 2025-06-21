from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd
import json, time, os, random

def get_local_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(
       service=Service(ChromeDriverManager().install()),
       options=options
    )

    return driver

def fetch_latam_preco(driver, origem, destino, data):

    url =(
      "https://www.latamairlines.com/br/pt/oferta-voos?"
      f"origin={origem}&destination={destino}&outbound={data}T15%3A00%3A00.000Z&"
      "adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED"
    )

    driver.get(url)
    time.sleep(20)

    for request in driver.requests:
          if "https://www.latamairlines.com/bff/air-offers/v2/offers/search" in request.url and request.response:
              try:
                  dados = json.loads(request.response.body.decode('utf-8'))

                  precos = []
                  for oferta in dados.get("content", []):
                      valor = oferta.get("summary", {}).get("brands", [])[0].get("price", {}).get("amount")
                      if valor:
                          precos.append(valor)

                  if precos:
                      return {
                          "origem": origem,
                          "destino": destino,
                          "data": data,
                          "precos": precos,
                          "menor_preco": min(precos) if precos else None,
                          "data_extracao": datetime.today().strftime("%Y-%m-%d"),
                      }

              except Exception as e:
                  print(f"Erro ao processar JSON da LATAM: {e}")

    print(f"Nenhum dado encontrado para {origem} -> {destino} em {data}")
    return None

def scrape(lista_rotas, datas):
    driver = get_local_driver()
    results = []

    for orig, dest in lista_rotas:
        for data in datas:
            print(f"Buscando {orig} -> {dest} em {data}")
            result = fetch_latam_preco(driver, orig, dest, data)
            if result:
                results.append(result)
            
            time.sleep(random.uniform(45, 60))

    driver.quit()

    os.makedirs("data/raw", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/raw/latam/latam_{timestamp}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nDados salvos em: {file_path}")

    csv_path = f"data/raw/latam/latam_{timestamp}.csv"

    rows = []
    for result in results:
        rows.append({
            "origem": result["origem"],
            "destino": result["destino"],
            "data": result["data"],
            "menor preço": result["menor_preco"],
            "data de extração": result["data_extracao"]
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"CSV salvo em: {csv_path}")

#rotas = [("GYN", "SSA")]
#datas = ["2025-07-01", "2025-08-01", "2025-09-01", "2025-10-01", "2025-11-01", "2025-12-01", "2026-01-01", "2026-02-01", "2026-03-01", "2026-04-01", "2026-05-01"]
#
#scrape(rotas, datas)