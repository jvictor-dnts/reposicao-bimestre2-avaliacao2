# Base — Controle De Treinos

Esta é a aplicação-base da avaliação de reposição.

Ela já possui CRUD de treinos com SQLite. O arquivo `auth.py` também já foi iniciado com Blueprint, mas a autenticação com `session` ainda precisa ser implementada.

## Executar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000`.

## Arquivos Principais

- `app.py`: rotas Flask.
- `auth.py`: módulo de autenticação já iniciado, ainda sem rotas cadastradas.
- `database.py`: funções de banco de dados.
- `templates/`: páginas HTML.

## Observação

Não substitua a aplicação por outro projeto. A tarefa é adaptar esta base para autenticação com `session`, completando o módulo `auth.py` e mantendo as rotas de treinos em `app.py`.

## Justificativas:
### 1. Por que as rotas de autenticação foram movidas para auth.py?
 pra deixar o código mais organizado e fácil de manutenção. usei os bluprint do flask para separar as coisas. app.py cuida só da lógica dos treinos, enquanto o auth.py centraliza o login, cadastro e logout.
 
### 2. Como a aplicação identifica o usuário logado usando session? 
 pela session do flask. quando o login dá certo, salva o ID dele em session ['usuario_id']. nas páginas seguintes, a aplicação só checa essa chave para saber quem está navegando.

### 3. Como o código impede que um usuário acesse treinos de outro usuário? 
em dois momentos na exibição quando o SQL só busca os treinos que têm o usuario_id igual ao da sessão atual. e também nas ações (editar, concluir, excluir). antes de qualquer alteração, o código valida se o treino realmente pertence a quem está logado. se não pertencer, a requisição é bloqueada com um erro 404.
