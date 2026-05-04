from pathlib import Path
import streamlit as st

ROOT_PATH = Path(__file__).resolve().parents[2] 

# =========================================================
# 🔹 CONSTANTES DE PÁGINA (PADRÃO GLOBAL)
# =========================================================
PAGINA_MG = "minas_gerais"
PAGINA_BRASIL = "brasil"
PAGINA_CAX = "caxambu"
PAGINA_MODELO = "modelo"
PAGINA_PROJETO = "projeto"

PAGINAS_LABEL = {
    PAGINA_BRASIL: "Brasil",
    PAGINA_MG: "MG",
    PAGINA_CAX: "Caxambu",
    PAGINA_MODELO: "Modelo",
    PAGINA_PROJETO: "Projeto",
}

# =========================================================
# 🔹 ESTADO GLOBAL DO APP
# =========================================================
def get_pagina() -> str:
    return st.session_state.get("pagina", PAGINA_CAX)


def set_pagina(pagina: str) -> None:
    st.session_state["pagina"] = pagina


# =========================================================
# 🔹 MENU SUPERIOR (NAVEGAÇÃO PRINCIPAL)
# =========================================================
def menu_paginas(prefix: str = "top") -> None:
    """
    Renderiza o menu de navegação.
    O prefix garante keys únicas (top / footer).
    """

    col1, col2, col3, col4, col5, _ = st.columns([1, 1, 1, 1, 1, 6])

    if col1.button(PAGINAS_LABEL[PAGINA_CAX], key=f"{prefix}_cax"):
        set_pagina(PAGINA_CAX)

    if col2.button(PAGINAS_LABEL[PAGINA_MG], key=f"{prefix}_mg"):
        set_pagina(PAGINA_MG)

    if col3.button(PAGINAS_LABEL[PAGINA_BRASIL], key=f"{prefix}_brasil"):
        set_pagina(PAGINA_BRASIL)

    if col4.button(PAGINAS_LABEL[PAGINA_MODELO], key=f"{prefix}_modelo"):
        set_pagina(PAGINA_MODELO)

    if col5.button(PAGINAS_LABEL[PAGINA_PROJETO], key=f"{prefix}_projeto"):
        set_pagina(PAGINA_PROJETO)
        
# =========================================================
# 🔹 MENU INFERIOR (NAVEGAÇÃO PRINCIPAL)
# =========================================================

def menu_paginas_footer():

    st.markdown(
        "<div style='margin-top:40px; margin-bottom:10px;'></div>",
        unsafe_allow_html=True
    )

    st.caption("Navegue entre as seções do dashboard:")

    menu_paginas(prefix="footer")

# =========================================================
# 🔹 BANNER
# =========================================================
def banner(caminho: str) -> None:
    caminho_completo = ROOT_PATH / caminho

    if not caminho_completo.exists():
        st.warning(f"Imagem não encontrada: {caminho}")
        return

    st.image(str(caminho_completo), width="stretch")
# =========================================================
# 🔹 LINHA DE CONTROLES (SEM NAVEGAÇÃO)
# =========================================================

def get_config_controles(pagina_atual: str, subaba: str) -> dict:
    """
    Define quais controles devem aparecer
    """

    is_cax = pagina_atual == "caxambu"

    return {
        "mostrar_geo": not is_cax,

        "mostrar_escola": (
            is_cax and subaba in [
                "estrutura socioeconômica",
                "desempenho",
                "desempenho x estrutura",
            ]
        ),

        "mostrar_materia": (
            is_cax and subaba in [
                "desempenho",
                "desempenho x estrutura",
            ]
        ),
    }


def linha_controles(
    subabas: list[str],
    pagina_atual: str,
    opcoes_geo: list[str],
    key_prefix: str,
    opcoes_ano: list[str] | None = None,
):

    # =========================
    # 🔹 ESTADO
    # =========================
    subaba = st.session_state.get(f"{key_prefix}_subaba", subabas[0])

    config = get_config_controles(pagina_atual, subaba)

    mostrar_geo = config["mostrar_geo"]
    mostrar_escola = config["mostrar_escola"]
    mostrar_materia = config["mostrar_materia"]

    # limpa geo se não usar
    if not mostrar_geo:
        st.session_state.pop(f"{key_prefix}_geo", None)

    # =========================
    # 🔹 CONTAGEM DE COLUNAS
    # =========================
    n_cols = 1  # subaba

    if mostrar_geo:
        n_cols += 1

    if opcoes_ano:
        n_cols += 1

    if mostrar_escola:
        n_cols += 1

    if mostrar_materia:
        n_cols += 1

    cols = st.columns(n_cols)

    i = 0

    # =========================
    # 🔹 SUBABA
    # =========================
    with cols[i]:
        subaba = st.selectbox(
            "",
            options=subabas,
            key=f"{key_prefix}_subaba",
        )
    i += 1

    # =========================
    # 🔹 GEO
    # =========================
    geo = None
    if mostrar_geo:
        with cols[i]:
            geo = st.selectbox(
                "Região" if pagina_atual == "minas_gerais" else "UF",
                options=[None] + opcoes_geo,
                format_func=lambda x: "Todos" if x is None else x,
                key=f"{key_prefix}_geo",
            )
        i += 1

    # =========================
    # 🔹 ANO
    # =========================
    ano = None
    if opcoes_ano:
        with cols[i]:
            ano = st.selectbox(
                "Ano",
                options=[None] + opcoes_ano,
                format_func=lambda x: "Todos" if x is None else x,
                key=f"{key_prefix}_ano",
            )
        i += 1

    # =========================
    # 🔹 ESCOLA
    # =========================
    escola = None
    if mostrar_escola:
        with cols[i]:
            escola = st.selectbox(
                "Tipo de escola",
                options=["Todas", "não informada", "pública", "privada"],
                key=f"{key_prefix}_escola",
            )
        i += 1

    # =========================
    # 🔹 MATÉRIA
    # =========================
    materia = None
    if mostrar_materia:
        from src.config import MAPA_MATERIA_LABEL_PARA_COLUNA

        with cols[i]:
            materia = st.selectbox(
                "Matéria",
                options=list(MAPA_MATERIA_LABEL_PARA_COLUNA.keys()),
                key=f"{key_prefix}_materia",
            )

    return subaba.lower(), geo, ano, escola, materia
# =========================================================
# 🔹 SIDEBAR ()
# =========================================================

def controles_sidebar_apoio(
    opcoes_geo=None,
    opcoes_ano=None,
    key_prefix="br",
    pagina_atual=None
):
    import streamlit as st

    st.sidebar.caption("Ajustes rápidos")

    # =========================================================
    # 🔹 SINCRONIZAÇÃO INICIAL
    # =========================================================
    if opcoes_geo and f"{key_prefix}_geo_sidebar" not in st.session_state:
        st.session_state[f"{key_prefix}_geo_sidebar"] = st.session_state.get(f"{key_prefix}_geo", None)

    if opcoes_ano and f"{key_prefix}_ano_sidebar" not in st.session_state:
        st.session_state[f"{key_prefix}_ano_sidebar"] = st.session_state.get(f"{key_prefix}_ano", None)

    if f"{key_prefix}_escola_sidebar" not in st.session_state:
        st.session_state[f"{key_prefix}_escola_sidebar"] = st.session_state.get(f"{key_prefix}_escola", "Todas")

    if f"{key_prefix}_materia_sidebar" not in st.session_state:
        st.session_state[f"{key_prefix}_materia_sidebar"] = st.session_state.get(f"{key_prefix}_materia", "Todas")

    # =========================================================
    # 🔹 CALLBACKS (NÃO QUEBRAM O TOPO)
    # =========================================================
    def sync_geo():
        st.session_state[f"{key_prefix}_geo"] = st.session_state[f"{key_prefix}_geo_sidebar"]

    def sync_ano():
        st.session_state[f"{key_prefix}_ano"] = st.session_state[f"{key_prefix}_ano_sidebar"]

    def sync_escola():
        st.session_state[f"{key_prefix}_escola"] = st.session_state[f"{key_prefix}_escola_sidebar"]

    def sync_materia():
        st.session_state[f"{key_prefix}_materia"] = st.session_state[f"{key_prefix}_materia_sidebar"]

    # =========================================================
    # 🔹 GEO (SÓ SE EXISTIR)
    # =========================================================
    if pagina_atual != "caxambu" and opcoes_geo:

        st.sidebar.selectbox(
            "Região" if pagina_atual == "minas_gerais" else "UF",
            [None] + opcoes_geo,
            format_func=lambda x: "Todos" if x is None else x,
            key=f"{key_prefix}_geo_sidebar",
            on_change=sync_geo
        )

    # =========================================================
    # 🔹 ANO (SÓ SE EXISTIR)
    # =========================================================
    if opcoes_ano:

        st.sidebar.selectbox(
            "Ano",
            [None] + opcoes_ano,
            format_func=lambda x: "Todos" if x is None else x,
            key=f"{key_prefix}_ano_sidebar",
            on_change=sync_ano
        )

    # =========================================================
    # 🔹 ESCOLA
    # =========================================================
    st.sidebar.selectbox(
        "Tipo de escola",
        ["Todas", "não informada", "pública", "privada"],
        key=f"{key_prefix}_escola_sidebar",
        on_change=sync_escola
    )

    # =========================================================
    # 🔹 MATÉRIA
    # =========================================================
    st.sidebar.selectbox(
        "Matéria",
        ["Todas", "Matemática", "Linguagens"],
        key=f"{key_prefix}_materia_sidebar",
        on_change=sync_materia
    )

# =========================================================
# 🔹 DIVISOR
# =========================================================
def divisor() -> None:
    st.markdown("---")

# =========================================================
# 🔹 ALINHAMENTO DO TEXTO
# =========================================================
def info_fullwidth(texto: str) -> None:
    st.markdown(
        f"""
        <div style='
            text-align: justify;
            width: 100%;
            padding: 12px;
            background-color: rgba(0,0,0,0.03);
            border-radius: 8px;
            margin-bottom: 10px;
        '>
            {texto}
        </div>
        """,
        unsafe_allow_html=True
    )

def get_estado_controles(key_prefix: str):
    subaba = st.session_state.get(f"{key_prefix}_subaba", "visão geral")
    return subaba


def banner_fullwidth_link(caminho: str, link: str) -> None:
    caminho_completo = ROOT_PATH / caminho

    if not caminho_completo.exists():
        st.warning(f"Imagem não encontrada: {caminho}")
        return

    import base64

    with open(caminho_completo, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    # HTML que torna a imagem clicável diretamente, sem JavaScript
    st.markdown(
        f"""
        <a href="{link}" target="_blank" style="display: block; width: 100%;">
            <img src="data:image/png;base64,{img_base64}" 
                 style="width: 100%; height: auto; display: block;">
        </a>
        """,
        unsafe_allow_html=True
    )