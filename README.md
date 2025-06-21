# 📊 Preço da Passagem x Lotação do Voo / Destino / Data

Este projeto analisa a relação entre os preços de passagens da LATAM e o histórico de ocupação dos voos (lotação) com base em dados públicos da ANAC. A análise busca identificar padrões entre a variação de preços e a taxa de ocupação para diferentes destinos e períodos.

---

## 👥 Integrantes

- Marcos Vinícius de Moraes  
- Patrick Fernandes Marins  
- Paulo Roberto Vieira

---

## ▶️ Como rodar o código

### Pré-requisitos

- Git
- Python 3.10+

### Passos

1. Clone o repositório:
    ```bash
    git clone https://github.com/Markoro-Original/extracao_automatica_passagem.git
    cd extracao_automatica_passagem
    ```

2. Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv

    #para Windows
    .\venv\Scripts\activate
    
    # Ou para Linux/macOS:
    source venv/bin/activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute o pipeline:
    ```bash
    python src/main.py
    ```

A execução seguirá a seguinte ordem:
1. Coleta de dados da ANAC (```extract_dados_anac.py```)
2. Filtro dos dados (```filtra_csv.py```)
3. Cálculo de demanda e ocupação e extração dos dados Latam (```demanda_anac.py``` e ```latam_scraper.py```)
4. Junção com preços LATAM (```merge.py```)
5. Análise dos dados da ANAC (```analise_anac.py```) - Fechar o gráfico para passar para a próxima etapa
6. Análise comparativa final (```analise.py```) - Fechar o gráfico para finalizar

## Licenças e fontes de dados
- ANAC – Agência Nacional de Aviação Civil
- LATAM – Coleta automatizada de dados de pesquisa de preços
- LGPD – Nenhum dado pessoal foi utilizado
- MIT License – Código aberto sob a licença MIT

## Slides da apresentação
Acesse a paresentação com os resultados da análise:

👉 [Visualizar slides no Genially](https://view.genially.com/6856afe17ac577972efd9aaa/interactive-content-precos-de-passagens-x-lotacaodestinomes)
