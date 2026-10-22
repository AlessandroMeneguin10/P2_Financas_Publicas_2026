from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dados"
OUT = ROOT / "resultados"
OUT.mkdir(exist_ok=True)
LEGACY = DATA / "base_p1_transcrita_nao_validada.csv"

# A tabela antiga é apenas referência para comparação com a P1; não é considerada validada.
df = pd.read_csv(LEGACY)
df.columns = [c.strip().lower() for c in df.columns]
for c in ["receita_total_p1_valor_sem_validacao", "despesa_total_p1_valor_sem_validacao"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

print("=== AUDITORIA DA BASE HISTÓRICA P1 ===")
print("Linhas:", len(df))
print("Anos:", df.ano.min(), "-", df.ano.max())
print("Municípios:", sorted(df.municipio.dropna().unique()))
print("Duplicatas município-ano:", df.duplicated(["ano", "municipio"]).sum())
print("Ausentes por coluna:", df.isna().sum())
print("ATENÇÃO: a coluna status registra que os valores precisam ser validados na fonte oficial.")

# Indicadores matemáticos sobre a série de referência. Interpretar somente depois de validar unidades.
df["saldo_p1_sem_validacao"] = df["receita_total_p1_valor_sem_validacao"] - df["despesa_total_p1_valor_sem_validacao"]
df.to_csv(OUT / "auditoria_base_p1.csv", index=False, encoding="utf-8-sig")

for col, title, ylabel, filename in [
    ("receita_total_p1_valor_sem_validacao", "Receita total — valores transcritos da P1 (não validados)", "Valor reportado na P1", "receita_p1_nao_validada.png"),
    ("despesa_total_p1_valor_sem_validacao", "Despesa total — valores transcritos da P1 (não validados)", "Valor reportado na P1", "despesa_p1_nao_validada.png"),
    ("saldo_p1_sem_validacao", "Diferença receita menos despesa — P1 (não validada)", "Diferença reportada", "saldo_p1_nao_validado.png")]:
    fig, ax = plt.subplots(figsize=(10, 5))
    for name, g in df.groupby("municipio"):
        g = g.sort_values("ano")
        ax.plot(g["ano"], g[col], marker="o", label=name)
    ax.set_title(title)
    ax.set_xlabel("Ano")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=180)
    plt.close(fig)

# Dados oficiais devem ser exportados em arquivo separado, sem sobrescrever a base antiga.
# Formato esperado para dados_municipios_oficiais.csv:
# ano,municipio,receita_total_nominal,despesa_total_nominal,transferencias_nominal,
# receita_tributaria_propria_nominal,populacao,fonte_url,data_acesso,observacao
official = DATA / "dados_municipios_oficiais.csv"
if official.exists():
    d = pd.read_csv(official)
    required = ["ano", "municipio", "receita_total_nominal", "despesa_total_nominal", "transferencias_nominal", "receita_tributaria_propria_nominal", "populacao"]
    missing = [c for c in required if c not in d.columns]
    if missing:
        raise ValueError(f"Colunas ausentes em dados_municipios_oficiais.csv: {missing}")
    print("=== AUDITORIA DOS DADOS OFICIAIS ===")
    print("Duplicatas município-ano:", d.duplicated(["ano", "municipio"]).sum())
    print("Ausentes:", d.isna().sum())
    d["saldo_orcamentario_nominal"] = d["receita_total_nominal"] - d["despesa_total_nominal"]
    d["receita_per_capita_nominal"] = d["receita_total_nominal"] / d["populacao"]
    d["despesa_per_capita_nominal"] = d["despesa_total_nominal"] / d["populacao"]
    d["participacao_transferencias"] = d["transferencias_nominal"] / d["receita_total_nominal"]
    d["autonomia_tributaria"] = d["receita_tributaria_propria_nominal"] / d["receita_total_nominal"]
    # Não calcula valores reais automaticamente: exige fator de deflação oficial validado.
    deflator_path = DATA / "deflator_ipca.csv"
    if deflator_path.exists():
        ipca = pd.read_csv(deflator_path)
        if not {"ano", "fator_deflacao"}.issubset(ipca.columns):
            raise ValueError("deflator_ipca.csv precisa ter ano e fator_deflacao")
        d = d.merge(ipca[["ano", "fator_deflacao"]], on="ano", how="left", validate="many_to_one")
        for c in ["receita_total_nominal", "despesa_total_nominal", "transferencias_nominal", "receita_tributaria_propria_nominal"]:
            d[c.replace("_nominal", "_real")] = d[c] * d["fator_deflacao"]
        print("Fatores IPCA incorporados. Confirme ano-base e fórmula no metadado antes de publicar.")
    d.to_csv(OUT / "dados_municipios_tratados.csv", index=False, encoding="utf-8-sig")
    print("Base oficial tratada exportada para", OUT / "dados_municipios_tratados.csv")
else:
    print("Ainda não há dados_municipios_oficiais.csv. Não foram inventados valores nem apresentados resultados oficiais.")
print("Arquivos de auditoria/gráficos salvos em:", OUT)
