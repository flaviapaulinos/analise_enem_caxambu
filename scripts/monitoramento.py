import pandas as pd

from src.monitoramento.drift import gerar_relatorio_drift
from src.monitoramento.quality import gerar_relatorio_qualidade
from src.monitoramento.utils import salvar_html


# =========================================================
# CARREGAR DADOS
# =========================================================

df = pd.read_parquet("dados/df_tratado.parquet")


# =========================================================
# SPLIT TEMPORAL
# =========================================================

df_ref = df[df["ano"] < 2024]

df_atual = df[df["ano"] == 2024]


# =========================================================
# COLUNAS MODELO
# =========================================================

colunas = [
    "SalMin",
    "Escola",
    "OcupPaisMedia",
    "EscolaridadePaisMedia",
    "Cel",
    "Comptdr",
    "PessoasResd"
]

df_ref = df_ref[colunas]

df_atual = df_atual[colunas]


# =========================================================
# DRIFT
# =========================================================

relatorio_drift = gerar_relatorio_drift(
    df_ref,
    df_atual
)

salvar_html(
    relatorio_drift,
    "drift_temporal_2024.html"
)


# =========================================================
# QUALIDADE
# =========================================================

relatorio_quality = gerar_relatorio_qualidade(
    df_ref,
    df_atual
)

salvar_html(
    relatorio_quality,
    "quality_temporal_2024.html"
)