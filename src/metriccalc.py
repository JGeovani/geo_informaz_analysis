import pandas as pd


def clear_value(value):
    return (
        str(value)
        .replace("R$", "")
        .replace(" ", "")
        .replace(".", "")
        .replace(",", ".")
    )

def q0_profitability_analysis(data):
    """
    Retorna:
    - Ranking de Rentabilidade por Categoria
    - Ranking de Rentabilidade por Produto
    - Sugestões de Otimização
    """

    # Preparar os dados
    sales = data["Transações Vendas"].copy()
    stock = data["Cadastro de Estoque"].copy()
    products = data["Cadastro Produtos"].copy()

    # Conversões
    sales["VALOR ITEM"] = sales["VALOR ITEM"].apply(clear_value).astype(float)
    sales["RECEITA"] = sales["VALOR ITEM"] * sales["QTD ITEM"]

    stock["VALOR ESTOQUE"] = stock["VALOR ESTOQUE"].apply(clear_value).astype(float)
    stock["VALOR UNITÁRIO"] = stock["VALOR ESTOQUE"] / stock["QTD ESTOQUE"]

    # Relacionar produto ao estoque
    products_stock = products.merge(stock, on="ID ESTOQUE", how="left")

    # Juntar tudo
    merged = sales.merge(products_stock, on="ID PRODUTO", how="left")

    # Calcular custo total por item
    merged["CUSTO TOTAL"] = merged["VALOR UNITÁRIO"] * merged["QTD ITEM"]
    merged["LUCRO"] = merged["RECEITA"] - merged["CUSTO TOTAL"]
    merged["RENTABILIDADE (%)"] = (merged["LUCRO"] / merged["RECEITA"]) * 100

    # Agrupamentos
    by_category = (
        merged.groupby("CATEGORIA")[["RECEITA", "CUSTO TOTAL", "LUCRO"]]
        .sum()
        .reset_index()
    )
    by_category["RENTABILIDADE (%)"] = (by_category["LUCRO"] / by_category["RECEITA"]) * 100
    by_category = by_category.sort_values(by="RENTABILIDADE (%)", ascending=False)

    by_product = (
        merged.groupby("NOME PRODUTO")[["RECEITA", "CUSTO TOTAL", "LUCRO"]]
        .sum()
        .reset_index()
    )
    by_product["RENTABILIDADE (%)"] = (by_product["LUCRO"] / by_product["RECEITA"]) * 100
    by_product = by_product.sort_values(by="RENTABILIDADE (%)", ascending=False)

    # Geração de sugestões automáticas
    suggestions = []

    # Categorias com baixa rentabilidade
    categorias_baixa = by_category[by_category["RENTABILIDADE (%)"] < 10]
    for _, row in categorias_baixa.iterrows():
        suggestions.append(f"Revisar estratégia de precificação ou fornecimento da categoria '{row['CATEGORIA']}' que possui rentabilidade de apenas {row['RENTABILIDADE (%)']:.1f}%.")

    # Produtos com prejuízo
    produtos_prejuizo = by_product[by_product["LUCRO"] < 0]
    for _, row in produtos_prejuizo.iterrows():
        suggestions.append(f"O produto '{row['NOME PRODUTO']}' está gerando prejuízo. Verifique custos ou reveja sua oferta.")

    # Produtos com alta receita mas rentabilidade baixa
    top_receita = by_product.sort_values(by="RECEITA", ascending=False).head(10)
    baixo_lucro = top_receita[top_receita["RENTABILIDADE (%)"] < 15]
    for _, row in baixo_lucro.iterrows():
        suggestions.append(f"O produto '{row['NOME PRODUTO']}' vende bem, mas tem rentabilidade baixa ({row['RENTABILIDADE (%)']:.1f}%). Considere ajustar o preço ou custo.")

    return by_category, by_product, suggestions

def q1_calc_total_value_per_category(data): #Calcule o valor total de venda dos produtos por categoria.
    products = data["Cadastro Produtos"]
    transactions = data["Transações Vendas"]

    # Padronize os nomes das colunas
    transactions.columns = transactions.columns.str.strip().str.upper()
    products.columns = products.columns.str.strip().str.upper()

    transactions["VALOR ITEM"] = (
        transactions["VALOR ITEM"]
        .astype(str)
        .replace('[R$ ]', '', regex=True)
        .str.replace('.', '')
        .str.replace(',', '.')
        .astype(float)
    )
    merged = transactions.merge(products, on="ID PRODUTO")
    result = (
        merged.groupby("CATEGORIA")["VALOR ITEM"]
        .sum()
        .reset_index()
        .sort_values(by="VALOR ITEM", ascending=False)
    )
    return result

def q2_calc_product_margin(data): # Calcule a margem dos produtos subtraindo o valor unitario pelo valor de venda.
    stock = data["Cadastro de Estoque"]
    transactions = data["Transações Vendas"]
    products = data["Cadastro Produtos"]

    transactions["VALOR ITEM"] = (
        transactions["VALOR ITEM"]
        .astype(str)
        .replace('[R$ ]', '', regex=True)
        .str.replace('.', '')
        .str.replace(',', '.')
        .astype(float)
    )
    stock["VALOR ESTOQUE"] = (
        stock["VALOR ESTOQUE"]
        .astype(str)
        .replace('[R$ ]', '', regex=True)
        .str.replace('.', '')
        .str.replace(',', '.')
        .astype(float)
    )
    products_in_stock = products.merge(stock, on="ID ESTOQUE", how="left")
    merged = transactions.merge(products_in_stock, on="ID PRODUTO", how="left")
    merged["margem"] = merged["VALOR ITEM"] - (merged["VALOR ESTOQUE"] / merged["QTD ESTOQUE"])
    result = (
        merged.groupby("ID PRODUTO")["margem"]
        .mean()
        .reset_index()
        .sort_values(by="margem", ascending=False)
    )
    return result

def q3_calc_client_ranking_by_quantity_per_month(data): #Calcule um ranking de clientes por quantidade de produtos comprados por mês.
    """Retorna ranking de clientes por quantidade de itens comprados por mês."""
    transactions = data["Transações Vendas"]
    clients = data["Cadastro Clientes"]
    transactions["DATA NOTA"] = pd.to_datetime(transactions["DATA NOTA"])
    transactions["AnoMes"] = transactions["DATA NOTA"].dt.to_period("M")
    merged = transactions.merge(clients, on="ID CLIENTE")
    result = (
        merged.groupby(["AnoMes", "NOME CLIENTE"])["QTD ITEM"]
        .sum()
        .reset_index()
        .sort_values(by=["AnoMes", "QTD ITEM"], ascending=[True, False])
    )
    return result

def q4_calc_ranking_suppliers_by_stock_by_month(data): #Calcule um ranking de fornecedores por quantidade de estoque disponivel por mês.
    stock = data["Cadastro de Estoque"]
    suppliers = data["Cadastro Fornecedores"]
    stock["DATA ESTOQUE"] = pd.to_datetime(stock["DATA ESTOQUE"])
    stock["AnoMes"] = stock["DATA ESTOQUE"].dt.to_period("M")
    merged = stock.merge(suppliers, on="ID FORNECEDOR")
    result = (
        merged.groupby(["AnoMes", "NOME FORNECEDOR"])["QTD ESTOQUE"]
        .sum()
        .reset_index()
        .sort_values(by=["AnoMes", "QTD ESTOQUE"], ascending=[True, False])
    )
    return result

def q5_calc_ranking_products_sales_per_month(data): #Calcule um ranking de produtos por quantidade de venda por mês.
    transactions = data["Transações Vendas"]
    transactions["DATA NOTA"] = pd.to_datetime(transactions["DATA NOTA"])
    transactions["AnoMes"] = transactions["DATA NOTA"].dt.to_period("M")
    result = (
        transactions.groupby(["AnoMes", "ID PRODUTO"])["QTD ITEM"]
        .sum()
        .reset_index()
        .sort_values(by=["AnoMes", "QTD ITEM"], ascending=[True, False])
    )
    return result

def q6_calc_product_ranking_salevalue_per_month(data): #Calcule um ranking de produtos por valor de venda por mês.
    transactions = data["Transações Vendas"]
    transactions["DATA NOTA"] = pd.to_datetime(transactions["DATA NOTA"])
    transactions["AnoMes"] = transactions["DATA NOTA"].dt.to_period("M")
    transactions["VALOR ITEM"] = (
        transactions["VALOR ITEM"]
        .astype(str)
        .replace('[R$ ]', '', regex=True)
        .str.replace('.', '')
        .str.replace(',', '.')
        .astype(float)
    )
    result = (
        transactions.groupby(["AnoMes", "ID PRODUTO"])["VALOR ITEM"]
        .sum()
        .reset_index()
        .sort_values(by=["AnoMes", "VALOR ITEM"], ascending=[True, False])
    )
    return result

def q7_calc_average_salesvalue_by_category_per_month(data): #Calcule a média de valor de venda por categoria de produto por mês.
    products = data["Cadastro Produtos"]
    transactions = data["Transações Vendas"]
    transactions["DATA NOTA"] = pd.to_datetime(transactions["DATA NOTA"])
    transactions["AnoMes"] = transactions["DATA NOTA"].dt.to_period("M")
    transactions["VALOR ITEM"] = (
        transactions["VALOR ITEM"]
        .astype(str)
        .replace('[R$ ]', '', regex=True)
        .str.replace('.', '')
        .str.replace(',', '.')
        .astype(float)
    )
    merged = transactions.merge(products, on="ID PRODUTO")
    result = (
        merged.groupby(["AnoMes", "CATEGORIA"])["VALOR ITEM"]
        .mean()
        .reset_index()
        .sort_values(by=["AnoMes", "VALOR ITEM"], ascending=[True, False])
    )
    return result

def q8_calc_profit_margin_ranking_by_category(data): #Calcule um ranking de margem de lucro por categoria.
    products = data["Cadastro Produtos"]
    transactions = data["Transações Vendas"]
    stock = data["Cadastro de Estoque"]
    transactions["VALOR ITEM"] = (
        transactions["VALOR ITEM"]
        .astype(str)
        .replace('[R$ ]', '', regex=True)
        .str.replace('.', '')
        .str.replace(',', '.')
        .astype(float)
    )
    stock["VALOR ESTOQUE"] = (
        stock["VALOR ESTOQUE"]
        .astype(str)
        .replace('[R$ ]', '', regex=True)
        .str.replace('.', '')
        .str.replace(',', '.')
        .astype(float)
    )
    merged = (
        transactions
        .merge(products, on="ID PRODUTO")
        .merge(stock, on="ID ESTOQUE", how="left")
    )
    merged["margem"] = merged["VALOR ITEM"] - (merged["VALOR ESTOQUE"] / merged["QTD ESTOQUE"])
    result = (
        merged.groupby("CATEGORIA")["margem"]
        .mean()
        .reset_index()
        .sort_values(by="margem", ascending=False)
    )
    return result

def q9_list_products_clients(data): #Liste produtos comprados por clientes.
    transactions = data["Transações Vendas"]
    clients = data["Cadastro Clientes"]
    products = data["Cadastro Produtos"]
    merged = (
        transactions
        .merge(clients, on="ID CLIENTE")
        .merge(products, on="ID PRODUTO")
    )
    result = (
        merged.groupby("NOME CLIENTE")["NOME PRODUTO"]
        .unique()
        .reset_index()
        .rename(columns={"NOME PRODUTO": "Produtos Comprados"})
    )
    return result

def q10_calc_product_ranking_by_stock(data): #Ranking de produtos por quantidade de estoque.
    stock = data["Cadastro de Estoque"]
    products = data["Cadastro Produtos"]
    merged = stock.merge(products, on="ID ESTOQUE")
    result = (
        merged.groupby("NOME PRODUTO")["QTD ESTOQUE"]
        .sum()
        .reset_index()
        .sort_values(by="QTD ESTOQUE", ascending=False)
    )
    return result
