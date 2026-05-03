import pandas as pd
import matplotlib
matplotlib.use('Agg')  # precisa disso pra funcionar sem tela aberta
import matplotlib.pyplot as plt
import os

# categorias e palavras-chave pra detectar automaticamente
CATEGORIAS = {
    "Alimentação": ["ifood", "rappi", "mcdonalds", "burger", "pizza", "padaria", "mercado", "supermercado", "restaurante"],
    "Transporte": ["uber", "99", "combustivel", "gasolina", "posto", "estacionamento", "onibus"],
    "Saúde": ["farmacia", "drogaria", "medico", "clinica", "hospital", "exame"],
    "Lazer": ["netflix", "spotify", "cinema", "teatro", "show", "steam", "jogos"],
    "Educação": ["udemy", "alura", "curso", "livro", "escola", "faculdade"],
    "Moradia": ["aluguel", "condominio", "luz", "agua", "internet", "gas"],
    "Roupas": ["zara", "renner", "hm", "shein", "roupa", "calcado"],
}

def categorizar(descricao):
    # tenta achar a categoria pela descrição da transação
    descricao = str(descricao).lower()
    for categoria, palavras in CATEGORIAS.items():
        for palavra in palavras:
            if palavra in descricao:
                return categoria
    return "Outros"  # se não achou nada, vai pra Outros

def ler_csv(caminho):
    # tenta ler o csv e detectar as colunas automaticamente
    df = pd.read_csv(caminho, sep=None, engine='python', encoding='utf-8-sig')
    df.columns = [col.strip().lower() for col in df.columns]
    return df

def processar_extrato(caminho):
    df = ler_csv(caminho)

    # tenta achar as colunas de descrição e valor
    col_descricao = None
    col_valor = None

    for col in df.columns:
        if any(p in col for p in ["descri", "histor", "memo", "detalhe"]):
            col_descricao = col
        if any(p in col for p in ["valor", "value", "amount", "quantia"]):
            col_valor = col

    # se não encontrou as colunas, usa as duas primeiras
    if col_descricao is None:
        col_descricao = df.columns[0]
    if col_valor is None:
        col_valor = df.columns[1]

    df["descricao"] = df[col_descricao].astype(str)
    df["valor"] = pd.to_numeric(
        df[col_valor].astype(str).str.replace(",", ".").str.replace("[^0-9.-]", "", regex=True),
        errors="coerce"
    )

    # remove linhas sem valor
    df = df.dropna(subset=["valor"])

    # categoriza cada transação
    df["categoria"] = df["descricao"].apply(categorizar)

    # separa receitas e despesas
    df["tipo"] = df["valor"].apply(lambda v: "Receita" if v > 0 else "Despesa")

    return df

def gerar_graficos(df, pasta_static):
    graficos = []

    # só pega as despesas pra mostrar no gráfico de pizza
    despesas = df[df["tipo"] == "Despesa"].copy()
    despesas["valor_abs"] = despesas["valor"].abs()

    if not despesas.empty:
        # gráfico de pizza por categoria
        por_categoria = despesas.groupby("categoria")["valor_abs"].sum()

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(por_categoria, labels=por_categoria.index, autopct="%1.1f%%", startangle=140)
        ax.set_title("Gastos por categoria")

        caminho = os.path.join(pasta_static, "grafico_pizza.png")
        plt.savefig(caminho, bbox_inches="tight")
        plt.close()
        graficos.append("grafico_pizza.png")

    return graficos

def calcular_resumo(df):
    total_receitas = df[df["tipo"] == "Receita"]["valor"].sum()
    total_despesas = df[df["tipo"] == "Despesa"]["valor"].abs().sum()
    saldo = total_receitas - total_despesas

    return {
        "total_receitas": round(total_receitas, 2),
        "total_despesas": round(total_despesas, 2),
        "saldo": round(saldo, 2),
        "total_transacoes": len(df)
    }