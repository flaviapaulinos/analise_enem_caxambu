import streamlit as st
import pandas as pd
import requests

from src.modelos.interpretacao import score_estrutural
from src.preprocessamento.categorias import (
    ORDEM_SAL_MIN,
    ORDEM_OCUPACAO,
    ORDEM_PAIS_ESCOLARIDADE,
    ORDEM_ESCOLA
)

from utils.layout import divisor


def render_aba_modelo():

    st.markdown(
        """ O modelo desenvolvido neste projeto tem como objetivo estimar a nota média esperada a partir de um perfil socioeconômico, com foco em uma interpretação estrutural e agregada. 
        
    Cada observação do modelo representa um grupo definido por:
    * faixa de renda familiar (em salários mínimos),
    * escolaridade dos responsáveis,
    * ocupação dos responsáveis,
    * tipo de escola frequentada,
    * características demográficas.
        
    Essa agregação reduz o ruído individual e permite analisar relações mais estáveis entre contexto social e desempenho educacional."""
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:

        st.subheader(" Capital Familiar (núcleo estrutural)")
        with st.container():
            salmin = st.selectbox("Renda familiar", ORDEM_SAL_MIN)

            col_f1, col_f2 = st.columns(2)
            with col_f1:
                ocup_pai = st.selectbox("Ocupação pai", ORDEM_OCUPACAO)
                esc_pai = st.selectbox("Escolaridade pai", ORDEM_PAIS_ESCOLARIDADE)
            with col_f2:
                ocup_mae = st.selectbox("Ocupação mãe", ORDEM_OCUPACAO)
                esc_mae = st.selectbox("Escolaridade mãe", ORDEM_PAIS_ESCOLARIDADE)

        st.subheader("💻 Acesso Tecnológico")
        with st.container():
            cel = st.selectbox("Celulares", [0, 1, 2, 3, "4 ou mais"])
            comp = st.selectbox("Computadores", [0, 1, 2, 3, "4 ou mais"])

        st.subheader("🏫 Institucional")
        with st.container():
            escola = st.selectbox("Tipo de escola", ORDEM_ESCOLA)

        st.subheader("🏠 Estrutura domiciliar")
        with st.container():
            pessoas = st.slider("Pessoas na residência", 1, 10, 3)

    with col2:
        st.markdown("""
        <div style="background-color:#f5f7fa; padding:18px; border-radius:10px; border:1px solid #e1e5ea">

        <b>📊 Sobre o modelo</b><br><br>

        O termo chave aqui é: <b>desempenho médio</b>.<br><br>
        
        Sabemos que indivíduos são complexos — e muitas vezes surpreendem.<br><br>
        
        Alguns superam desafios socioeconômicos significativos. Outros, mesmo com estrutura, enfrentam obstáculos que os dados não capturam.<br><br>
        
        Por isso, este modelo não descreve indivíduos, mas <b>padrões médios de grupos</b>.<br><br>
        
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # TRATAMENTO
    # =========================
    def tratar(x):
        return 4 if x == "4 ou mais" else x

    cel = tratar(cel)
    comp = tratar(comp)

    def cat_num(v, ordem):
        return ordem.index(v)

    ocup_media = (
        cat_num(ocup_pai, ORDEM_OCUPACAO) +
        cat_num(ocup_mae, ORDEM_OCUPACAO)
    ) / 2

    esc_media = (
        cat_num(esc_pai, ORDEM_PAIS_ESCOLARIDADE) +
        cat_num(esc_mae, ORDEM_PAIS_ESCOLARIDADE)
    ) / 2

    # =========================
    # DATAFRAME
    # =========================
    dados = pd.DataFrame([{
        "SalMin": salmin,
        "Escola": escola,
        "OcupPaisMedia": ocup_media,
        "EscolaridadePaisMedia": esc_media,
        "Cel": cel,
        "Comptdr": comp,
        "PessoasResd": pessoas
    }])

    divisor()

    # =========================
    # PREDIÇÃO (API)
    # =========================
    if st.button("Prever nota"):

        try:
            url = "https://analise-enem-caxambu-1.onrender.com/predict"

            payload = dados.iloc[0].to_dict()

            response = requests.post(url, json=payload)

            if response.status_code == 200:

                resultado = response.json()
                nota = resultado["nota_prevista"]

                st.success(f"Nota prevista: {nota:.1f}")

                # 🔥 SCORE LOCAL (mantido)
                # Aqui você pode manter se quiser ou remover depois
                st.info("Score estrutural disponível apenas na versão local do modelo.")

            else:
                st.error(f"Erro na API: {response.text}")

        except Exception as e:
            st.error(f"Erro na requisição: {e}")