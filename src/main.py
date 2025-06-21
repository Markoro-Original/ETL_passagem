import subprocess
import os
import sys

base_path = os.path.dirname(__file__)

def run(script_path):
    full_path = os.path.join(base_path, script_path)
    print(f"\nExecutando: {script_path}\n")
    subprocess.run([sys.executable, full_path], check=True)

run("collectors/extract_dados_anac.py")
run("utils/filtra_csv.py")
run("collectors/demanda_anac.py") #também roda o script latam_scraper.py
run("merge/merge.py")
run("analise/analise_anac.py")
run("analise/analise.py")