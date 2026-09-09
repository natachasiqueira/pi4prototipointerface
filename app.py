import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuração inicial da página (Layout expandido)
st.set_page_config(page_title="Painel de Aprendizagem", layout="wide")

# 2. Geração de Dados Mockados (Simulando o output do modelo do seu colega)
@st.cache_data
def carregar_dados():
    # QUANDO O PROJETO AVANÇAR, VOCÊ APAGARÁ O CÓDIGO ABAIXO E USARÁ APENAS:
    # return pd.read_csv("nome_do_arquivo_anonimizado_do_diogo.csv")
    
    # --- INÍCIO DOS DADOS FALSOS ---
    np.random.seed(42)
    n_alunos = 250
    dados = {
        'ID_Aluno': range(1, n_alunos + 1),
        'Ano_Escolar': np.random.choice(['6º Ano', '7º Ano', '8º Ano', '9º Ano'], n_alunos),
        'Nota_Geral': np.random.uniform(4.0, 10.0, n_alunos).round(1),
        'Faltas': np.random.randint(0, 30, n_alunos),
        'Risco_Socioeconomico': np.random.choice(['Alto', 'Médio', 'Baixo'], n_alunos, p=[0.2, 0.3, 0.5]),
        'Perfil_Aprendizagem': np.random.choice(
            ['Avançado', 'Intermediário', 'Atenção/Reforço'], 
            n_alunos, 
            p=[0.25, 0.55, 0.20] # 20% dos alunos no grupo de risco
        )
    }
    return pd.DataFrame(dados)
    # --- FIM DOS DADOS FALSOS ---

df = carregar_dados()

# 3. Barra Lateral (Filtros Interativos)
st.sidebar.header("Filtros de Análise")
ano_selecionado = st.sidebar.multiselect(
    "Selecione o Ano Escolar:",
    options=df['Ano_Escolar'].unique(),
    default=df['Ano_Escolar'].unique()
)

# Aplicando o filtro no dataframe
df_filtrado = df[df['Ano_Escolar'].isin(ano_selecionado)]

# 4. Cabeçalho e KPIs (Indicadores Principais)
st.title("📊 Análise e Clusterização de Perfis de Aprendizagem")
st.markdown("Visão estratégica para personalização do ensino e intervenção pedagógica na EMEB Guilhermina de Couto Oliveira.")
st.divider()

# Calculando KPIs para destacar no topo
total_alunos = len(df_filtrado)
alunos_risco = len(df_filtrado[df_filtrado['Perfil_Aprendizagem'] == 'Atenção/Reforço'])
pct_risco = (alunos_risco / total_alunos) * 100 if total_alunos > 0 else 0
media_faltas = df_filtrado['Faltas'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total de Alunos Analisados", total_alunos)
col2.metric("Alunos em Perfil de Atenção (Reforço)", alunos_risco, f"{pct_risco:.1f}% da base", delta_color="inverse")
col3.metric("Média de Faltas Geral", f"{media_faltas:.1f} dias")

st.divider()

# 5. Área de Gráficos (Storytelling Visual)
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("Distribuição por Perfil de Aprendizagem")
    # Contagem de alunos por cluster
    df_perfil = df_filtrado['Perfil_Aprendizagem'].value_counts().reset_index()
    df_perfil.columns = ['Perfil', 'Quantidade']
    
    # Uso intencional de cor: Destacando o perfil de "Atenção" em vermelho
    cores_perfis = {'Avançado': '#1f77b4', 'Intermediário': '#d3d3d3', 'Atenção/Reforço': '#d62728'}
    
    fig_barras = px.bar(
        df_perfil, 
        x='Perfil', 
        y='Quantidade', 
        color='Perfil',
        color_discrete_map=cores_perfis,
        text_auto=True
    )
    # Limpando o design (fundo branco, sem grades pesadas)
    fig_barras.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig_barras, use_container_width=True)

with col_grafico2:
    st.subheader("Relação: Notas x Faltas")
    # Gráfico de dispersão para ver como as faltas afetam a nota, colorindo pelo perfil
    fig_dispersao = px.scatter(
        df_filtrado, 
        x='Faltas', 
        y='Nota_Geral', 
        color='Perfil_Aprendizagem',
        color_discrete_map=cores_perfis,
        opacity=0.7
    )
    fig_dispersao.update_layout(template="plotly_white")
    st.plotly_chart(fig_dispersao, use_container_width=True)

# 6. Tabela de Detalhamento no final
st.subheader("Detalhamento de Alunos para Intervenção")
st.markdown("Lista de estudantes classificados no perfil **Atenção/Reforço** para planejamento de atividades direcionadas.")
df_atencao = df_filtrado[df_filtrado['Perfil_Aprendizagem'] == 'Atenção/Reforço'].sort_values(by='Nota_Geral')
st.dataframe(df_atencao, use_container_width=True, hide_index=True)