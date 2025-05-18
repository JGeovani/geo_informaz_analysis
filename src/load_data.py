import pandas as pd

def load_data(file_path="data/Case_Infomaz_Base_de_Dados.xlsx"):
    tabs = [
        "Guia",
        "Cadastro Produtos",
        "Cadastro Clientes",
        "Cadastro de Estoque",
        "Cadastro Fornecedores",
        "Transações Vendas"
    ]
    try:
        data = pd.read_excel(
            file_path,
            sheet_name=tabs,
            engine="openpyxl",
            header=1
        )
        print("Dados carregados com sucesso!")
        return data
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        raise
    except ValueError as error:
        print(f"Erro ao carregar abas: {error}")
        raise
