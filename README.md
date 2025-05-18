# Infomaz - Sistema de Análise de Dados

Este projeto é um sistema de análise de dados para o case Infomaz, desenvolvido em Python utilizando **Streamlit** para interface web. Ele permite visualizar dados de diferentes cadastros e gerar relatórios e cálculos analíticos de forma simples e interativa pelo navegador.

## Funcionalidades

- Visualização de dados das abas:
  - Cadastro Produtos
  - Cadastro Clientes
  - Cadastro de Estoque
  - Cadastro Fornecedores
  - Transações Vendas
- Relatórios e cálculos automáticos, incluindo:
  - Valor total de venda por categoria
  - Margem dos produtos
  - Ranking de clientes, fornecedores e produtos
  - Média de vendas por categoria/mês
  - Produtos comprados por cliente
  - Relatórios de rentabilidade com sugestões de otimização para maximizar lucros
  - E outros

## Como executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/jgeovani/geo_infomaz-analysis.git
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
   > Se não houver um arquivo `requirements.txt`, instale manualmente:
   ```bash
   pip install streamlit pandas openpyxl
   ```

3. **Coloque o arquivo de dados Excel em `data/Case_Infomaz_Base_de_Dados.xlsx`**  
   (ou ajuste o caminho no código, se necessário).

4. **Execute a aplicação:**
   ```bash
   streamlit run main.py
   ```

5. **Acesse pelo navegador:**  
   O Streamlit irá mostrar um endereço como `http://localhost:8501` ou `http://SEU_IP_LOCAL:8501`.  
   - Use `http://localhost:8501` para acessar do próprio computador.
   - Para que outras pessoas na mesma rede acessem, use o endereço de IP local mostrado pelo Streamlit (ex: `http://192.168.1.10:8501`).

   > Para acesso externo (fora da sua rede), será necessário configurar o roteador ou usar serviços de deploy como [Streamlit Cloud](https://streamlit.io/cloud).

## Estrutura do Projeto

```
geo_informaz_analysis/
│
├── main.py
├── requirements.txt
├── .gitignore
├── data/
│   └── Case_Infomaz_Base_de_Dados.xlsx
├── src/
│   ├── load_data.py
│   ├── metriccalc.py
│   └── __init__.py
└── README.md
```

## Observações

- Não inclua a pasta `venv` no repositório. Cada desenvolvedor pode criar seu próprio ambiente virtual.
- O arquivo `requirements.txt` garante que todos tenham as mesmas dependências.

## Licença

Este projeto é apenas para fins educacionais e de demonstração.

---

Desenvolvido por jgeovani utilizando Visual Studio Code.