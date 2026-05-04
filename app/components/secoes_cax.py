import streamlit as st
import pandas as pd

from utils.helpers_ui import (
    plot,
    txt_distribuicao,
    txt_escolaridade_escola,
    txt_renda_pais,
    txt_bubble_relacao,
    txt_renda_nota_simples,
    txt_desigualdade,
    txt_tecnologia,
    txt_conclusao
)

from src.config import MAPA_MATERIA_LABEL_PARA_COLUNA

from src.visualizacao.graficos_dash import (
    analise_acesso_tecnologia_cax,
    analise_mobilidade_ranking,
    boxplot_notas,
    bubble_chart_4d,
    evolucao_demografica_cax,
    grafico_barras_percentual,
    grafico_coluna_empilhada_percentual,
    grafico_combinado_notas_renda,
    grafico_comparativo_pais,
    grafico_comparativo_escola_privada_pais,
    grafico_distribuicao_itens_domiciliares,
    grafico_linha_nota_media_renda,
    grafico_nota_media_por_categoria_escola_ano,
    grafico_notas_linhas_max,
    grafico_notas_violino,
    grafico_raca_por_renda_barras,
    grafico_renda_responsavel,
    tabela_plotly_gradiente,
    tabela_notas_maximas,
    treemap_escola_renda,
    treemap_nota_escola,
)

# =========================================================
# SOCIAL / DEMOGRÁFICA — CAX
# =========================================================

def render_subaba_social_demografica_cax(
    df_d_seg: pd.DataFrame,
    df_r_seg: pd.DataFrame,
    df_merged: pd.DataFrame,
    df_d_uni: pd.DataFrame,
    
):
    container_categoria = st.container()

    with container_categoria:
        col_titulo, col_radio = st.columns([2, 4], gap="xsmall")

        with col_titulo:
            st.markdown("##### Distribuição Percentual")

        with col_radio:
            st.caption(
                "selecione uma das opções para análise dessa categoria."
            )
            categoria = st.radio(
                "",
                options=["escola", "sal_min", "sexo", "cor_raca", "faixa_etaria"],
                format_func=lambda x: {
                    "sexo": "sexo",
                    "cor_raca": "cor/raça",
                    "escola": "escola",
                    "sal_min": "renda mensal familiar (salários mínimos)",
                    "faixa_etaria": "faixa etária",
                }[x],
                horizontal=True,
                key="cax_social_categoria",
            )
            

    col1, col2 = st.columns([1, 1], gap="small")
    
    with col1:


        fig_barras, _ = grafico_barras_percentual(
            df=df_d_seg,
            categoria=categoria,
            escopo="caxambu",
            weight_col="participantes",
        )
        plot(fig_barras, "cax_social_barras")

        st.caption(
            """Análise
        
Escola: A elevada proporção de participantes que não informaram o tipo de escola cursada no ensino médio merece atenção. 
Uma hipótese plausível é a dificuldade de classificação por parte de estudantes com trajetória híbrida (rede pública e privada), 
o que pode levar à não resposta por não se identificarem plenamente com apenas uma das categorias."""
        )
        st.caption(
                "Renda: Em Caxambu, 76% dos participantes declararam renda familiar mensal de até 3 salários mínimos. "
    "Embora as faixas de 3 a 5 e de 5 a 10 salários mínimos também apresentem participação relevante, "
    "elas permanecem abaixo da distribuição observada em Minas Gerais."
        )

        st.caption(
            "Em relação à cor/raça, o perfil dos participantes de Caxambu é semelhante ao observado no sul de Minas: "
"predominância de pessoas brancas (64%), seguidas por pessoas negras (34%)."
        )
            
       

       
        
    with col2:
      
        fig_evolucao_renda, _ = evolucao_demografica_cax(
            df=df_d_uni,
            variavel=categoria,
            escopo="caxambu",
        )
        plot(fig_evolucao_renda, "cax_evolucao_renda")
        st.caption(
            """Análise: 
Escola: Apenas 10% dos participantes informaram ter cursado o ensino médio em escola privada. Na análise temporal, observa-se queda na renda média entre estudantes de escola pública (-9,4%) e privada (-8,9%) entre 2021 e 2024. Em contraste, o grupo que não informou o tipo de escola apresentou crescimento expressivo (+46,5%), contudo, esse resultado é fortemente influenciado pelo baixo número de observações em 2024 (n=5), o que limita sua robustez estatística. Em Minas Gerais, a evolução da renda média ao longo dos anos foi observada apenas entre os participantes que não informaram o tipo de escola cursada."""
        )
        
        st.caption(
            """ Análise:
            
Cor/Raça: No recorte por cor/raça, observa-se redução da renda média entre participantes brancos (-16,5%) e negros (-10,3%) no período analisado. Por outro lado, há crescimento expressivo entre os grupos que se declararam amarelos e aqueles que não informaram cor/raça; entretanto, essa variação deve ser interpretada com cautela devido ao tamanho amostral extremamente reduzido ao longo da série. Em Minas Gerais, por contraste, houve queda generalizada da renda média entre todas as raças."""
        )
               
                

    col3, col4 = st.columns([1, 1], gap="small")

    with col3:

            
        fig_emp, _ = grafico_coluna_empilhada_percentual(
            df=df_d_seg,
            eixo_x="sal_min",
            eixo_cor="escola",
            escopo="caxambu",
            weight_col="participantes",
        )
        plot(fig_emp, "cax_social_emp")

        st.caption(
            """ Análise: 
            
Em Caxambu, observa-se maior participação relativa de estudantes de escolas privadas em comparação aos demais recortes: na faixa de renda de 3 a 5 salários mínimos, a participação de estudantes de escolas privadas já supera a de escolas públicas. Em Minas Gerais e no Brasil, esse predomínio ocorre apenas a partir da faixa de 5 a 10 salários mínimos."""
    )
        
    with col4:
        
        fig_tab, _ = tabela_plotly_gradiente(
            df=df_d_seg,
            linha="ano",
            coluna=categoria,
            valor="renda_media",
            escopo="caxambu",
        )
        plot(fig_tab, "cax_social_tab")


    fig_priv, _ = grafico_comparativo_escola_privada_pais(
        df=df_d_seg,
        escopo="caxambu",
        weight_col="participantes",
    )
    plot(fig_priv, "cax_social_priv")
    
    st.caption(
        """ Análise:
        
O gráfico compara como a escolaridade dos pais influencia a opção por escola privada dentro de uma mesma faixa de renda. Em Caxambu, assim como no estado de Minas e no Brasil, é constatado que quanto maior a escolaridade dos pais, maior a chance do participante cursar escola privada (dentro de uma mesma faixa de renda)."""
            )

    col5, col6 = st.columns([1.5, 1], gap="small")

    with col5:
        fig_comp, _ = grafico_raca_por_renda_barras(
            df=df_d_seg,
            ano_selecionado=None,
            escopo="caxambu",
            weight_col="participantes",
        )
        plot(fig_comp, "cax_raca_renda")
        st.caption(
            """ Análise:
            
Em Caxambu, Minas e no Brasil as pessoas que se identificam como brancas têm maior participação nas faixas de renda mais altas. No município a prevalência de pessoas com a renda entre 1 e 3 salários mínimos está aproximadamente 10 pontos percentuais acima do observado no estado, em contrapartida há menor participação nas faixas de renda mais altas.  Em Caxambu, dentre os participantes do Enem, as pessoas que se identificam como amarelas, tiveram maior participação nas faixas de rendas mais altas. É importante frisar que a representatividade dessa raça (23 participantes) é bem inferior, quando comparada com as raças branca e negra. """
            )

    with col6:
        fig_tree, _ = treemap_escola_renda(
            df=df_d_seg,
            escopo="caxambu",
        )
        plot(fig_tree, "cax_social_tree")
       
    container_pais = st.container()
    with container_pais:
        col_titulo, col_radio = st.columns([1, 2], gap="small")

        with col_titulo:
            st.markdown("##### Comparativo Pais/Responsáveis - Caxambu")

        with col_radio:
            tipo_comp = st.radio(
                "",
                options=["escolaridade", "ocupacao"],
                format_func=lambda x: {
                    "escolaridade": "Escolaridade",
                    "ocupacao": "Ocupação",
                }[x],
                horizontal=True,
                key="cax_social_pais_toggle",
            )     

    col7, col8 = st.columns([2, 1], gap="xxsmall")

    with col7:
        fig_comp, _ = grafico_comparativo_pais(
            df=df_d_seg,
            tipo=tipo_comp,
            ano_selecionado=None,
            escopo="caxambu",
            weight_col="participantes",
        )
        plot(fig_comp, "cax_social_comp")
        
        st.caption(
            """ Análise:
            
A escolaridade dos responsáveis, assim como no resto do país, se concentra em: ensino fundamental e médio. Constata-se que as mães possuem o nível de escolaridade um pouco superior. O percentual de responsáveis com ensino superior ou pós-graduação está um pouco abaixo da média do estado."""
        )
        st.caption(
             """ Análise:
Já em relação a ocupação do responsáveis, há uma diferenciação entre mães e pais. A ocupação dos pais se divide principalmente em: rural, atividades que exigem ensino básico,  atividades que exigem ensino médio/ ou técnico e atividades manuais que exigem ensino fundamental. Muito similar a distribuição do país. A ocupação das mães se concentra em atividades básicas e atividades que exigem ensino médio, ou ensino técnico (padrão que pode ser visto no resto do país também)."""
            )
        #colocar link para dicionário

    with col8:
        fig_renda, _ = grafico_renda_responsavel(
            df=df_d_seg,
            variavel=tipo_comp,
            ano_selecionado=None,
            escopo="cax",
            weight_col="participantes",
        )
        plot(fig_renda, "cax_social_renda")
        st.caption(
            """ Análise:
O padrão da distribuição de renda por ocupação dos responsáveis reflete o restante do país (maior renda para atividades que exigem maior escolaridade). Nota-se que a renda média em Caxambu (por tipo de ocupação) é menor que a média de Minas e do país (exceto para atividades rurais). A diferença é maior especialmente para atividades que exigem ensino médio/ou atividades técnicas e ocupações que exigem ensino superior. """
            )

    graficos_socioecono = grafico_distribuicao_itens_domiciliares(
            df=df_d_uni,
            ano_selecionado=None,
            escopo="cax",
        )
    plot(graficos_socioecono, "cax_graficos_socioecono")
    st.caption(
        """ Análise:
A maior parte dos participantes reside em domicílios com 2 a 3 pessoas e possui geladeira. Cerca de um terço não possui máquina de lavar roupas, e o principal meio de acesso à informação é o telefone celular. Apenas 41 participantes não possuem celular em casa, enquanto 187 não possuem televisão."""
            )
st.caption(
"As interpretações devem considerar o tamanho amostral em cada grupo, especialmente nas categorias "
"com baixa frequência, onde variações percentuais podem ser amplificadas."
)


    



# =========================================================
# NOTAS — CAXAMBU
# =========================================================

def render_subaba_notas_cax(
    df_r_seg,
    df_merged,
    df_r_uni,
    escola,
    materia,
):

    st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)

    materia_coluna = None
    if materia:
        materia_coluna = MAPA_MATERIA_LABEL_PARA_COLUNA[materia]

    if escola and escola != "Todas":
        df_r_seg = df_r_seg[df_r_seg["escola"] == escola]

    fig_box, _ = boxplot_notas(
        df_r_uni,
        escopo="caxambu",
    )
    plot(fig_box, "cax_box")
    

    fig_tab, _ = tabela_notas_maximas(
        df=df_r_seg,
        escopo="cax",
    )
    plot(fig_tab, "cax_tab")
    
    st.caption(
        """
        Análise do Desempenho de Caxambu:

Matemática — principal oportunidade: Maior desvio padrão (em ambos)
Alta dispersão: base mais fraca / topo competitivo

Existe um grupo de alto desempenho competitivo com o estado

Redação
Menor desigualdade interna

Em várias disciplinas:

	* Intervalos mais compactos
	* Menos extremos

Indicador de maior equidade educacional

Caxambu apresenta desempenho geral próximo ao de Minas Gerais, com destaque para a consistência dos resultados e menor desigualdade entre os participantes. Embora as médias sejam ligeiramente inferiores, observa-se a presença de alunos com desempenho elevado, especialmente em redação e matemática, indicando potencial competitivo. Os principais desafios concentram-se na elevação do desempenho da base de alunos, mais do que na formação de alta performance."""
        )

  

# =========================================================
# DESEMPENHO X ESTRUTURA — CAX
# =========================================================

def render_subaba_desempenho_estrutura_cax(
    df_d_seg,
    df_r_seg,
    df_merged,
    df_r_uni,
    df_agg_21_23,
    df_21_23,
    
    escola,
    materia,
):

    st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)

    materia_coluna = None
    if materia:
        materia_coluna = MAPA_MATERIA_LABEL_PARA_COLUNA[materia]

    col1, col2 = st.columns([2.3, 1], gap="small")

    with col1:

        fig_bubble, _, _ = bubble_chart_4d(
            df=df_merged,
            escopo="cax",
        )
        plot(fig_bubble, "cax_bubble")
        txt_bubble_relacao()
    

    with col2:

        fig_linha_renda, _ = grafico_linha_nota_media_renda(
            df=df_21_23,
            escopo="cax",
        )
        plot(fig_linha_renda, "cax_linha")
    st.caption(
        """
        
        Análise:
             
    A análise da relação entre renda familiar e desempenho evidencia um padrão consistente tanto em Caxambu quanto em Minas Gerais: quanto maior a renda, maior tende a ser a nota dos participantes. Caxambu tem maior engajamento, mesmo com menos recursos (em relação a média do estado)
    Existe um ganho consistente de desempenho conforme aumenta a renda, especialmente na faixa de 10 a 15 salários mínimos. A relação não é perfeitamente linear nas rendas mais altas devido ao baixo número de participantes, o que aumenta a volatilidade Caxambu performa como o esperadado dado o nível de renda."""
        )
                   

    fig_cat, _ = grafico_nota_media_por_categoria_escola_ano(
        df_agg_21_23,
        categoria="sal_min",
        escopo="cax",
    )
    plot(fig_cat, "cax_cat")
    st.caption(
        """ Análise:
        
    Em Caxambu assim como Minas, observa-se que em todas as faixas de renda, alunos de escolas privadas superam os de escolas públicas (notas médias). A diferença pode ultrapassar 80 a 100 pontos nas faixas mais baixas.
O tipo de escola atua como um fator adicional relevante, além da renda."""
    )

    col3, col4 = st.columns(2)

    with col3:
        fig_linhas, _ = grafico_notas_linhas_max(
            df=df_r_seg,
            escopo="cax",
        )
        plot(fig_linhas, "cax_linhas")

    with col4:
        fig_violino = grafico_notas_violino(
            df=df_r_uni,
            escopo="cax",
        )
        plot(fig_violino, "cax_violino")
        
    st.caption(
        """ Análise:

Observa-se confirmação dos fatos já observados - escolas privadas apresentam as maiores médias em todas as disciplinas.
Em Caxambu, as escolas públicas apresentam médias mais baixas, porém com menor variação interna. A diferença entre redes não está apenas no topo, mas em toda a distribuição de desempenho."""
    )
        
    col5, col6 = st.columns(2)
    
    with col5: 
        fig_tec, _ = analise_acesso_tecnologia_cax(
            df=df_merged,
            escopo="cax",
            weight_col="participantes",
        )
        plot(fig_tec, "cax_tec")
        st.caption(
            """Análise:
            
A relação entre acesso a tecnologia e desempenho em Caxambu mostra:
* Estabilidade no número de celulares por domicílio (~2,6 a 2,7)
* Queda no número médio de computadores (0,92 → 0,70)
Notas médias relativamente estáveis (~544 a 553 pontos)
O acesso a computadores diminuiu ao longo do tempo, sem impacto direto proporcional nas médias, sugerindo que outros fatores (como renda e escolaridade) têm maior peso no desempenho."""
        )
    
    with col6:
        fig_tree, _ = treemap_nota_escola(
            df=df_r_seg,
            materia=materia,
            escopo="cax",
        )
        plot(fig_tree, "cax_tree")
        
        st.caption(
        
        "O gap institucional não é um problema local, se repete em Minas e Brasil"    
        )
     
    st.caption(

        """
        Análise:
        
Os dados indicam que o desempenho educacional em Caxambu está fortemente associado a fatores socioeconômicos, especialmente renda e tipo de escola. Ainda assim, o município demonstra capacidade de alcançar resultados elevados nos grupos com melhores condições, além de apresentar padrões consistentes de progressão educacional.

👉 Em termos estratégicos:

O desafio principal está na redução das desigualdades associadas à renda e à rede de ensino
O potencial de alto desempenho já está presente e pode ser expandido."""    
        )

    

   
