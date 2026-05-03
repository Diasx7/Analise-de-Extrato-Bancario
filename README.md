# Analisador de Extrato Bancário

Ferramenta feita em Python que lê o extrato bancário em CSV, categoriza os gastos automaticamente e mostra gráficos e resumo financeiro no navegador.

## O que ele faz

- Lê arquivos CSV exportados do banco
- Categoriza as transações automaticamente por palavra-chave (iFood → Alimentação, Uber → Transporte, etc.)
- Mostra um gráfico de pizza com os gastos por categoria
- Exibe resumo com total de receitas, despesas e saldo
- Lista as 10 maiores despesas do período

## Tecnologias usadas

- Python 3
- Flask
- Pandas
- Matplotlib
- Bootstrap 5

## Como rodar

1. Clone o repositório
2. Crie e ative o ambiente virtual
3. Instale as dependências
4. Rode o projeto

```powershell
git clone https://github.com/Diasx7/Analise-de-Extrato-Bancario.git
cd Analise-de-Extrato-Bancario
python -m venv venv
venv\Scripts\Activate
pip install flask pandas matplotlib reportlab openpyxl
python app.py
```

Acesse no navegador: `http://localhost:5000`

## Formato do CSV

O arquivo precisa ter pelo menos uma coluna de descrição e uma de valor. A maioria dos bancos exporta nesse formato direto no app ou internet banking.
