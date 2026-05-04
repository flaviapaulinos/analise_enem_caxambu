from __future__ import annotations
import streamlit as st

from services.loaders import carregar_bases_cax
from utils.helpers_filtros import filtrar_df
from utils.helpers_ui import plot
from utils.layout import (
    linha_controles, 
    divisor, 
    info_fullwidth, 
    get_estado_controles, 
    set_pagina, 
    PAGINA_CAX,
    PAGINA_MG, 
    PAGINA_BRASIL, 
    PAGINA_MODELO, 
    PAGINA_PROJETO
)

from components.secoes_cax import (
    render_subaba_social_demografica_cax,
    render_subaba_notas_cax,
    render_subaba_desempenho_estrutura_cax,  
)

from src.visualizacao.graficos_dash import (
    criar_painel_indicadores_gerais,
    gerar_mapa_enem,
    grafico_evolucao_temporal_acurado,
)
def controles_sidebar_apoio(
    opcoes_geo=None,
    opcoes_ano=None,
    key_prefix="cax",
    pagina_atual=None
):
    import streamlit as st

    st.sidebar.caption("Ajustes rápidos")

    # =========================================================
    # 🔹 CALLBACKS
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
    # 🔹 GEO (SOMENTE SE EXISTIR)
    # =========================================================
    if pagina_atual != "caxambu" and opcoes_geo:

        # sincroniza valor inicial
        if f"{key_prefix}_geo_sidebar" not in st.session_state:
            st.session_state[f"{key_prefix}_geo_sidebar"] = st.session_state.get(f"{key_prefix}_geo", None)

        st.sidebar.selectbox(
            "Região" if pagina_atual == "minas_gerais" else "UF",
            [None] + opcoes_geo,
            format_func=lambda x: "Todos" if x is None else x,
            key=f"{key_prefix}_geo_sidebar",
            on_change=sync_geo
        )

    else:
        # 🔥 limpa estado para evitar bug
        st.session_state.pop(f"{key_prefix}_geo", None)
        st.session_state.pop(f"{key_prefix}_geo_sidebar", None)

    # =========================================================
    # 🔹 ANO
    # =========================================================
    if opcoes_ano:

        if f"{key_prefix}_ano_sidebar" not in st.session_state:
            st.session_state[f"{key_prefix}_ano_sidebar"] = st.session_state.get(f"{key_prefix}_ano", None)

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
    if f"{key_prefix}_escola_sidebar" not in st.session_state:
        st.session_state[f"{key_prefix}_escola_sidebar"] = st.session_state.get(f"{key_prefix}_escola", "Todas")

    st.sidebar.selectbox(
        "Tipo de escola",
        ["Todas", "não informada", "pública", "privada"],
        key=f"{key_prefix}_escola_sidebar",
        on_change=sync_escola
    )

    # =========================================================
    # 🔹 MATÉRIA
    # =========================================================
    if f"{key_prefix}_materia_sidebar" not in st.session_state:
        st.session_state[f"{key_prefix}_materia_sidebar"] = st.session_state.get(f"{key_prefix}_materia", "Todas")

    st.sidebar.selectbox(
        "Matéria",
        ["Todas", "Matemática", "Linguagens"],
        key=f"{key_prefix}_materia_sidebar",
        on_change=sync_materia
    )
    




def render_dashboard_cax():

    bases = carregar_bases_cax()

    df_d_seg = bases["demografico"]
    df_r_seg = bases["resultados"]
    df_m = bases["merged"]
    df_r_uni = bases["resultados_uni"]
    df_d_uni = bases["dados_uni"]
    df_21_23_agg = bases["21_23"]
    df_21_23_uni = bases["21_23_uni"]

    anos = sorted(df_d_seg["ano"].dropna().astype(str).unique())


  
    anos = sorted(df_d_seg["ano"].dropna().astype(str).unique())


    subaba_display = st.session_state.get("cax_subaba", "visão geral")

# =========================================================
# HEADER + CONTEXTO
# =========================================================

    if subaba_display == "visão geral":
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            info_fullwidth(
                """Quanto o contexto social influencia a nota no ENEM?<br><br>
    
        🔎 Navegque pelas abas para analisar os fatores socioeconômicos e sua relação com o desempenho dos participantes do Enem ao longo da série histórica (2021–2024), com foco em Caxambu.<br><br>
        A abordagem combina análise descritiva, agregações ponderadas por participantes e visualizações multivariadas para identificar padrões estruturais na desigualdade educacional e modelo preditivo.
        
        
        **Mais informações na página Projeto.**"""
            )

        with col2:
            st.markdown(
                """
            <div style="background-color:#01818078; solid #01818078">
            
            <b>Contexto e interpretação</b>
            
            O Brasil é diverso e complexo — e os dados refletem apenas parte dessa realidade.<br>
            
            O questionário socioeconômico do Enem é uma fonte rica de informações sobre o contexto dos participantes. Quando analisado em conjunto com o desempenho nas provas, permite observar como fatores estruturais influenciam os resultados educacionais. Ainda assim, é importante reconhecer que os indivíduos são mais complexos do que qualquer base de dados pode representar.<br>
            Por isso, as análises deste projeto são feitas em nível agregado, considerando grupos e médias — uma forma de compreender padrões estruturais, sem perder de vista que cada trajetória é única.
            
            </div>
                    """,
                    unsafe_allow_html=True
                )
        
        st.subheader("Visão Geral: Enem — Caxambu (2021–2024)")
        
        info_fullwidth(
        """Visão consolidada do ENEM em Minas Gerais ao longo da série histórica. """
        )
    
    elif subaba_display == "estrutura socioeconômica":
        
        st.subheader("Análise Social e Demográfica — Caxambu")
        
        info_fullwidth(
            """Análise da estrutura socioeconômica dos participantes, considerando distribuições percentuais e relações entre variáveis como renda familiar, 
        escolaridade e ocupação dos responsáveis."""
        )
    
    elif subaba_display == "desempenho":
        st.subheader("Análise de Desempenho — Caxambu")
        st.caption("Base analítica: Enem 2021–2024")
        
        info_fullwidth(
            """Análise do desempenho dos participantes, com foco na identificação de padrões regionais, diferenças por tipo de escola e distribuição das notas.  
            Parte das visualizações utiliza dados agregados, enquanto outras utilizam amostra de dados individuais para análise de distribuição."""
        )
    
    elif subaba_display == "desempenho x estrutura":
        st.subheader("Desempenho e Estrutura Socioeconômica — Caxambu")
        st.caption("Base analítica: ENEM 2021–2024")
        info_fullwidth(
            """Análise integrada da relação entre fatores socioeconômicos e desempenho ao longo do tempo, permitindo observar padrões estruturais persistentes 
        e possíveis mecanismos associados às desigualdades educacionais."""
        )
    # =========================================================
    # CONTROLES (SIDEBAR + TOPO)
    # =========================================================
    
    # Sidebar (apoio)
    controles_sidebar_apoio(
        opcoes_geo=None,
        key_prefix="cax",
        opcoes_ano=anos,
        pagina_atual="caxambu"
    )
    
    
    subaba, geo, ano, escola, materia = linha_controles(
        subabas=["visão geral", "estrutura socioeconômica", "desempenho", "desempenho x estrutura"],
        pagina_atual="caxambu",
        opcoes_geo=[],  # 🔥 vazio mesmo
        key_prefix="cax",
        opcoes_ano=anos,
    )
    
 
    
    df_d_seg = filtrar_df(df_d_seg, ano=ano, escola=escola)
    df_r_seg = filtrar_df(df_r_seg, ano=ano, escola=escola)
    df_m = filtrar_df(df_m, ano=ano, escola=escola)
    df_r_uni = filtrar_df(df_r_uni, ano=ano, escola=escola)
    df_d_uni = filtrar_df(df_d_uni, ano=ano, escola=escola)
    df_21_23_agg = filtrar_df(df_21_23_agg, ano=ano, escola=escola)
    df_21_23_uni = filtrar_df(df_21_23_uni, ano=ano, escola=escola)



    # =========================================================
    # VISÃO GERAL
    # =========================================================
    if subaba == "visão geral":
        
        st.caption(
            "Os gráficos podem levar alguns instantes para carregar devido ao volume de dados processados. "
            "Aguarde o carregamento completo para uma melhor experiência."
        )

        col1, col2 = st.columns(2)

        with col1:
            fig, _ = criar_painel_indicadores_gerais(
                df_notas_filtrado=df_r_seg,
                df_demografico_filtrado=df_d_seg,
                escopo="cax",
                ano_selecionado=None,
            )
            plot(fig, "cax_visao_painel")

        with col2:
            fig_evolucao, _ = grafico_evolucao_temporal_acurado(
                df=df_m,
                escopo="cax",
                materias_selecionadas=None,
                weight_col="participantes",
                titulo=None,
            )
            plot(fig_evolucao, "cax_visao_evolucao")
            
        st.caption(
            
            """A análise dos indicadores educacionais no período de 2021 a 2024
            
Caxambu apresenta um desempenho geral próximo ao de Minas Gerais, com algumas diferenças estruturais importantes — especialmente no perfil socioeconômico — e pontos positivos relevantes no engajamento e na performance em áreas específicas.

No período analisado, Minas Gerais contabilizou mais de 1,39 milhão de participantes, enquanto Caxambu registrou 3.644 participantes. A nota média geral do estado foi de 558 pontos, ligeiramente superior à média de Caxambu (548,3). Essa diferença, no entanto, deve ser interpretada à luz das condições socioeconômicas.

Caxambu apresenta renda média familiar (2,87) inferior à de Minas Gerais (3,41), além de menor acesso a recursos, como computadores (0,78 em média, contra 0,93 no estado) e índice de consumo (0,319 vs. 0,328). Ainda assim, o município demonstra um importante diferencial: a taxa de presença média é superior, atingindo 76,1% frente a 71,2% no estado. Esse dado é particularmente relevante, pois indica maior engajamento dos participantes locais — fator que contribui diretamente para a qualidade e representatividade dos resultados.

Caxambu apresenta escolas com desempenho máximo equivalente ao das melhores do estado, evidenciando capacidade de alta performance. Ao mesmo tempo, embora exista variação entre escolas, a distribuição geral dos resultados sugere um sistema relativamente consistente, com diferenças mais concentradas nos extremos do que no conjunto dos participantes.

🎯 Desempenho acadêmico

Ao observar as médias por área do conhecimento, nota-se que:

Redação é o principal destaque de Caxambu, com média (654,3) ligeiramente superior à de Minas Gerais (653,6), indicando boa competência em habilidades de expressão escrita.
Em Matemática, a diferença é moderada (553,3 em Caxambu vs. 562,0 no estado), sugerindo espaço para avanço, mas sem distorções significativas.
Em Ciências Humanas, Linguagens e Ciências da Natureza, as médias de Caxambu são inferiores às do estado, porém seguem o mesmo padrão de distribuição, indicando alinhamento estrutural com o desempenho estadual.

*Análises mais aprofundadas nas abas específicas

"""
        )
        
        st.caption(
                "O índice de consumo foi construído a partir da normalização de bens e infraestrutura domiciliar (ex.: eletrodomésticos, veículos e acesso a serviços), agregados em uma métrica única entre 0 e 1. Esse indicador atua como proxy de nível socioeconômico, permitindo capturar dimensões de bem-estar não refletidas diretamente pela renda declarada."
            )
        
        

    # =========================================================
    # SOCIAL
    # =========================================================
    elif subaba == "estrutura socioeconômica":
        
        st.caption(
            "Os gráficos podem levar alguns instantes para carregar devido ao volume de dados processados. "
            "Aguarde o carregamento completo para uma melhor experiência."
        )

        divisor()
        
        render_subaba_social_demografica_cax(
            df_d_uni=df_d_uni,
            df_d_seg=df_d_seg,
            df_r_seg=df_r_seg,
            df_merged=df_m,
        )

    # =========================================================
    # DESEMPENHO
    # =========================================================
    elif subaba == "desempenho":
        
        st.caption(
            "Os gráficos podem levar alguns instantes para carregar devido ao volume de dados processados. "
            "Aguarde o carregamento completo para uma melhor experiência."
        )
        
        divisor()
        
        render_subaba_notas_cax(
            df_r_seg=df_r_seg,
            df_merged=df_m,
            df_r_uni=df_r_uni,
            escola=escola,
            materia=materia,
        )
        
        st.info(
        """
        Alguns gráficos utilizam amostras individuais para distribuição.
        """
        )

    # =========================================================
    # NOVA SUBABA
    # =========================================================
    elif subaba == "desempenho x estrutura":
        
        st.caption(
            "Os gráficos podem levar alguns instantes para carregar devido ao volume de dados processados. "
            "Aguarde o carregamento completo para uma melhor experiência."
        )
        
        divisor()
        
        render_subaba_desempenho_estrutura_cax(
            df_d_seg=df_d_seg,
            df_r_seg=df_r_seg,
            df_merged=df_m,
            df_r_uni=df_r_uni,
            df_agg_21_23=df_21_23_agg,   
            df_21_23=df_21_23_uni,      
            escola=escola,
            materia=materia,
        )

        