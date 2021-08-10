from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
uri = os.environ.get('DATABASE_URL')
if uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

class Pokemon(db.Model): # table pokemon
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    imagem = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(255), nullable=False)
    
    def __init__(self, nome, imagem, descricao, tipo):
        self.nome = nome
        self.imagem = imagem
        self.descricao = descricao
        self.tipo = tipo

@app.route('/')
def index():
    pokedex = Pokemon.query.all()
    return render_template('index.html', pokedex=pokedex)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
       pokemon = Pokemon(
           request.form['nome'],
           request.form['imagem'],
           request.form['descricao'],
           request.form['tipo']
       )
       db.session.add(pokemon)
       db.session.commit()
       return redirect('/')

@app.route('/<id>')
def get_by_id(id):
    pokemon = Pokemon.query.get(id)
    return render_template('index.html', pokemonDelete=pokemon)

@app.route('/delete/<id>')
def delete(id):
    pokemon = Pokemon.query.get(id)
    db.session.delete(pokemon)
    db.session.commit()
    return redirect('/')

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    pokemon = Pokemon.query.get(id)
    if request.method == 'POST':
        pokemon.nome = request.form['nome']
        pokemon.imagem = request.form['imagem']
        pokemon.descricao = request.form['descricao']
        pokemon.tipo = request.form['tipo']
        db.session.commit()
        return redirect('/')
    return render_template('index.html', pokemon=pokemon)

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    tipo = request.form['search']
    pokedex = Pokemon.query.filter(Pokemon.tipo.ilike(f'%{tipo}%')).all()
    return render_template('index.html', pokedex=pokedex)

@app.route('/filter/<param>')
def filter_param(param):
    pokedex = Pokemon.query.filter_by(tipo=param).all()
    return render_template('index.html', pokedex=pokedex)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    