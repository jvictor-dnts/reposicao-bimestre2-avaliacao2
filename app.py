from flask import Flask, render_template, request, redirect, url_for, session, abort
from auth import auth_bp
import database

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-sessao'

app.register_blueprint(auth_bp)
database.criar_tabelas()

@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    treinos = database.listar_treinos_por_usuario(session['usuario_id'])
    return render_template('index.html', treinos=treinos)

@app.route('/treinos/novo', methods=['GET', 'POST'])
def novo_treino():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        usuario_id = session['usuario_id']

        database.criar_treino(titulo, descricao, usuario_id)
        return redirect(url_for('index'))

    return render_template('novo_treino.html')

@app.route('/treinos/editar/<int:id>', methods=['GET', 'POST'])
def editar_treino(id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    treino = database.buscar_treino_por_id(id)

    if not treino or treino['usuario_id'] != session['usuario_id']:
        abort(404)

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        database.atualizar_treino(id, titulo, descricao)
        return redirect(url_for('index'))

    return render_template('editar_treino.html', treino=treino)

@app.route('/treinos/concluir/<int:id>')
def concluir_treino(id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    treino = database.buscar_treino_por_id(id)

    if not treino or treino['usuario_id'] != session['usuario_id']:
        abort(404)

    database.marcar_concluido(id)
    return redirect(url_for('index'))

@app.route('/treinos/excluir/<int:id>')
def excluir_treino(id):
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))

    treino = database.buscar_treino_por_id(id)

    if not treino or treino['usuario_id'] != session['usuario_id']:
        abort(404)

    database.deletar_treino(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)