from flask import Flask, render_template, request, redirect, url_for
import os
from analisador import processar_extrato, gerar_graficos, calcular_resumo

app = Flask(__name__)

# pasta onde os csvs vão ser salvos
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analisar", methods=["POST"])
def analisar():
    # pega o arquivo enviado pelo formulário
    arquivo = request.files["arquivo"]

    if arquivo.filename == "":
        return redirect(url_for("index"))

    # salva o arquivo na pasta uploads
    caminho = os.path.join(app.config["UPLOAD_FOLDER"], arquivo.filename)
    arquivo.save(caminho)

    # processa o extrato
    df = processar_extrato(caminho)

    # gera os gráficos na pasta static
    graficos = gerar_graficos(df, "static")

    # calcula o resumo
    resumo = calcular_resumo(df)

    # pega as 10 maiores despesas
    maiores_gastos = (
        df[df["tipo"] == "Despesa"]
        .nlargest(10, "valor", keep="all")
        .assign(valor=lambda x: x["valor"].abs())
        [["descricao", "categoria", "valor"]]
        .to_dict(orient="records")
    )

    # manda tudo pra página de resultado
    return render_template(
        "resultado.html",
        resumo=resumo,
        graficos=graficos,
        maiores_gastos=maiores_gastos,
        transacoes=df[["descricao", "categoria", "valor", "tipo"]].to_dict(orient="records")
    )

if __name__ == "__main__":
    app.run(debug=True)