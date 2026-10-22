#!/usr/bin/env python3
"""Baixa arquivos oficiais de apoio para a P2. Não substitui a curadoria contábil.

Uso: python codigo/baixar_dados_oficiais.py
Requer: requests, pandas
O script preserva os arquivos brutos; não converte valores nem imputa ausências.
"""
from pathlib import Path
import json, time, sys
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "dados" / "brutos_oficiais"
RAW.mkdir(parents=True, exist_ok=True)
YEARS = list(range(2015, 2025))  # janela inicial comum; confirmar cobertura final nos metadados
BASE = "https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt"
SICONFI_ENTES = {"Canindé": "2302800", "Quixadá": "2311306"}
SWISS_FILES = {
    "estatisticas_financeiras_natureza_funcao.csv": "https://www.data.finance.admin.ch/static/assets/datasets/fs_dashboard/fir_art_funk.csv",
    "estatisticas_financeiras_tabelas_regulares.csv": "https://www.data.finance.admin.ch/static/assets/datasets/fs_dashboard/standardauswertung.csv",
    "estatisticas_financeiras_municipios.xlsx": "https://www.data.finance.admin.ch/static/assets/datasets/fs_dashboard/gdn-e.xlsx",
    "estatisticas_GFS_governo_geral.xlsx": "https://www.data.finance.admin.ch/static/assets/datasets/gfs_dashboard/staat-e.xlsx",
}
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "P2-FSP-academic-research/1.0", "Accept": "application/json,text/csv,application/octet-stream,*/*"})


def save_response(url, path, params=None):
    r = SESSION.get(url, params=params, timeout=90)
    r.raise_for_status()
    path.write_bytes(r.content)
    return r.url, r.status_code, len(r.content), r.headers.get("content-type", "")


def download_siconfi():
    log = []
    for municipality, code in SICONFI_ENTES.items():
        for year in YEARS:
            path = RAW / f"siconfi_dca_{municipality.lower()}_{year}.json"
            if path.exists() and path.stat().st_size > 0:
                log.append({"fonte": "SICONFI DCA", "ente": municipality, "ano": year, "status": "já existia", "arquivo": str(path.relative_to(ROOT))})
                continue
            url = f"{BASE}/dca"
            params = {"an_exercicio": year, "id_ente": code}
            try:
                final_url, status, size, ctype = save_response(url, path, params)
                # O conteúdo é preservado integralmente. Verificação leve de estrutura JSON.
                payload = json.loads(path.read_text(encoding="utf-8"))
                log.append({"fonte": "SICONFI DCA", "ente": municipality, "ano": year, "status": status, "bytes": size, "content_type": ctype, "arquivo": str(path.relative_to(ROOT)), "url_consultada": final_url, "chaves_resposta": ",".join(payload.keys()) if isinstance(payload, dict) else "lista"})
            except Exception as e:
                if path.exists(): path.unlink()
                log.append({"fonte": "SICONFI DCA", "ente": municipality, "ano": year, "status": "falha", "erro": str(e), "url": url})
            time.sleep(1.1)  # documentação oficial limita a uma requisição por segundo
    pd.DataFrame(log).to_csv(RAW / "log_download_siconfi.csv", index=False, encoding="utf-8-sig")


def download_swiss():
    log = []
    for filename, url in SWISS_FILES.items():
        path = RAW / filename
        try:
            final_url, status, size, ctype = save_response(url, path)
            log.append({"fonte": "Federal Finance Administration (FFA/EFV)", "status": status, "bytes": size, "content_type": ctype, "arquivo": str(path.relative_to(ROOT)), "url": final_url})
        except Exception as e:
            log.append({"fonte": "Federal Finance Administration (FFA/EFV)", "status": "falha", "arquivo": filename, "url": url, "erro": str(e)})
    pd.DataFrame(log).to_csv(RAW / "log_download_suica.csv", index=False, encoding="utf-8-sig")


def main():
    try:
        download_siconfi()
        download_swiss()
    except KeyboardInterrupt:
        print("Interrompido. Os arquivos já baixados foram preservados.")
    print(f"Arquivos/logs em: {RAW}")
    print("ATENÇÃO: baixar não equivale a validar. Conferir anexos, unidade, cobertura, homologação/retificação e classificações antes de construir as séries analíticas.")

if __name__ == "__main__":
    main()
