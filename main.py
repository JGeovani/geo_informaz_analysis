import streamlit as st
from src.load_data import load_data
from src.metriccalc import (
    q0_profitability_analysis,
    q1_calc_total_value_per_category,
    q2_calc_product_margin,
    q3_calc_client_ranking_by_quantity_per_month,
    q4_calc_ranking_suppliers_by_stock_by_month,
    q5_calc_ranking_products_sales_per_month,
    q6_calc_product_ranking_salevalue_per_month,
    q7_calc_average_salesvalue_by_category_per_month,
    q8_calc_profit_margin_ranking_by_category,
    q9_list_products_clients,
    q10_calc_product_ranking_by_stock,
)
import os

st.set_page_config(page_title="Infomaz: Análise de Dados", layout="wide")

@st.cache_data
def get_data():
    file_path = os.path.join("data", "Case_Infomaz_Base_de_Dados.xlsx")
    return load_data(file_path)

data = get_data()

# CSS customizado para o tema Peers Consulting + Technology
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #003366;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    }
    .css-18e3th9 {
        background-color: #0056b3;
    }
    .st-bb, .st-cb, .st-eb, .st-c6, .st-cg {
        background-color: #000000 !important;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stButton>button {
        background-color: #003366;
        color: #fff;
        border-radius: 6px;
        border: none;
        padding: 0.5em 1.5em;
        font-weight: 600;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: #fff;
    }
    .stSelectbox>div>div {
        background-color: #000;
        border-radius: 6px;
    }
    .stSidebar {
        background-color: #003366;
    }
    .stSidebar .css-1d391kg {
        color: #fff;
    }
    h1, .stTitle {
        color: #003366;
        font-weight: 700;
        letter-spacing: 1px;
    }
    h2, .stHeader {
        color: #0056b3;
        font-weight: 600;
    }
    .stDataFrame {
        background-color: #000;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Infomaz")
st.subheader("Sistema de Análise de Dados")

st.markdown(
    """
    <div style='text-align: right; margin-bottom: 10px;'>
        <img src='https://peers.com.br/wp-content/uploads/2025/03/logo.svg' alt='Peers Consulting + Technology' width='180'/>
        <br>
        <span style='font-size: 14px; color: #888;'>Análise de Dados e Desenvolvimento Web por <b>Peers Consulting + Technology</b></span>
    </div>
    """,
    unsafe_allow_html=True
)

menu = st.sidebar.selectbox(
    "Escolha uma opção:",
    ["Relatórios de Rentabilidade", "Dados das Tabelas", "Cálculos de Métricas"]
)

if menu == "Dados das Tabelas":
    st.header("Dados das Tabelas")
    tab = st.selectbox(
        "Escolha a tabela desejada:",
        [
            "Cadastro Produtos",
            "Cadastro Clientes",
            "Cadastro de Estoque",
            "Cadastro Fornecedores",
            "Transações Vendas"
        ]
    )
    st.dataframe(data[tab])

elif menu == "Cálculos de Métricas":
    st.header("Cálculos das Métricas")
    options = {
        "Valor Total de Venda por Categoria": q1_calc_total_value_per_category,
        "Margem dos Produtos": q2_calc_product_margin,
        "Ranking dos Clientes por Quantidade Comprada por Mês": q3_calc_client_ranking_by_quantity_per_month,
        "Ranking dos Fornecedores por Estoque por Mês": q4_calc_ranking_suppliers_by_stock_by_month,
        "Ranking dos Produtos por Quantidade Vendida por Mês": q5_calc_ranking_products_sales_per_month,
        "Ranking Produtos por Valor de Venda por Mês": q6_calc_product_ranking_salevalue_per_month,
        "Média de Valor de Venda por Categoria por Mês": q7_calc_average_salesvalue_by_category_per_month,
        "Ranking de Margem de Lucro por Categoria": q8_calc_profit_margin_ranking_by_category,
        "Lista de Produtos Comprados por Cliente": q9_list_products_clients,
        "Ranking de Produtos por Estoque": q10_calc_product_ranking_by_stock,
    }
    choice = st.selectbox("Escolha a métrica: ", list(options.keys()))
    result = options[choice](data)
    if isinstance(result, dict):
        for key, df in result.items():
            st.subheader(key)
            st.dataframe(df)
    else:
        st.dataframe(result)

elif menu == "Relatórios de Rentabilidade":
    st.header("Relatório de Análise de Rentabilidade de Produtos e Categorias")

    # Não há necessidade de selectbox, pois só há uma opção
    report_result = q0_profitability_analysis(data)

    # Exibe os resultados de forma organizada
    if isinstance(report_result, tuple) and len(report_result) == 3:
        by_category, by_product, suggestions = report_result

        st.subheader("Ranking de Rentabilidade por Categoria")
        st.dataframe(by_category)

        st.subheader("Ranking de Rentabilidade por Produto")
        st.dataframe(by_product)

        # Identifica as categorias e produtos de maior e menor rentabilidade
        highest_category = by_category.iloc[0, 0]
        lowest_category = by_category.iloc[-1, 0]
        highest_product = by_product.iloc[0, 0]
        lowest_product = by_product.iloc[-1, 0]

        st.subheader("Sugestões de Otimização")
        st.markdown(f"""
        **Estratégias para Maximizar Lucros:**

        - **Acompanhe tendências de demanda:** Monitore periodicamente as vendas de cada categoria e produto, identificando rapidamente variações no comportamento de compra dos clientes.
        - **Produtos de maior rentabilidade:** Foque em <span style="color:#FFFF00"><b>{highest_product}</b></span>, investindo em divulgação, estoque e negociações especiais para ampliar ainda mais sua margem.
        - **Produtos de menor rentabilidade:** Reavalie <span style="color:#b30000"><b>{lowest_product}</b></span>, analisando se ajustes de preço, renegociação com fornecedores ou até descontinuação podem ser necessários.
        - **Categorias de maior rentabilidade:** Invista em <span style="color:#FFFF00"><b>{highest_category}</b></span>, priorizando compras e promoções para manter o bom desempenho.
        - **Categorias de menor rentabilidade:** Analise estratégias para <span style="color:#b30000"><b>{lowest_category}</b></span>, como renegociação de custos, revisão de preços ou campanhas para aumentar o giro.
        - **Otimize o estoque:** Reduza estoques de itens com baixa margem e baixo giro, liberando capital para investir em produtos de maior rentabilidade e demanda crescente.
        - **Negocie com fornecedores:** Busque melhores condições para produtos estratégicos e de baixa margem, fortalecendo parcerias e reduzindo custos.
        - **Ajuste a precificação:** Revise periodicamente os preços, considerando custos, concorrência e sensibilidade dos clientes, para garantir margens saudáveis sem perder competitividade.
        - **Use dados para decisões rápidas:** Implemente rotinas de análise para identificar rapidamente mudanças de padrão e agir de forma proativa.
        """, unsafe_allow_html=True)
    else:
        st.dataframe(report_result)