from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "tarefas.db"


def conectar():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def criar_banco():
    conn = conectar()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = conectar()

    tarefas = conn.execute("""
        SELECT *
        FROM tarefas
        ORDER BY concluida ASC, id DESC
    """).fetchall()

    conn.close()

    return render_template("index.html", tarefas=tarefas)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form.get("titulo", "").strip()

    if titulo:
        conn = conectar()

        conn.execute("""
            INSERT INTO tarefas (titulo, concluida)
            VALUES (?, 0)
        """, (titulo,))

        conn.commit()
        conn.close()

    return redirect("/")


@app.route("/concluir/<int:id>", methods=["POST"])
def concluir(id):
    conn = conectar()

    tarefa = conn.execute("""
        SELECT concluida
        FROM tarefas
        WHERE id = ?
    """, (id,)).fetchone()

    if tarefa:
        novo_estado = 0 if tarefa["concluida"] else 1

        conn.execute("""
            UPDATE tarefas
            SET concluida = ?
            WHERE id = ?
        """, (novo_estado, id))

        conn.commit()

    conn.close()

    return redirect("/")


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conn = conectar()

    conn.execute("""
        DELETE FROM tarefas
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    criar_banco()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
