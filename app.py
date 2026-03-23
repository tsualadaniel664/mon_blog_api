from flask import Flask, request, render_template, redirect, url_for
from models import db, Article
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Page principale : tableau de tous les articles
@app.route('/articles-html')
def show_articles():
    articles = Article.query.all()
    return render_template('articles.html', articles=articles)

# Recherche
@app.route('/articles-recherche')
def search_articles():
    titre = request.args.get('titre')
    auteur = request.args.get('auteur')
    categorie = request.args.get('categorie')

    query = Article.query
    if titre:
        query = query.filter(Article.titre.ilike(f"%{titre}%"))
    if auteur:
        query = query.filter(Article.auteur.ilike(f"%{auteur}%"))
    if categorie:
        query = query.filter(Article.categorie.ilike(f"%{categorie}%"))

    articles = query.all()
    return render_template('articles.html', articles=articles)

# Ajouter un article
@app.route('/articles-ajouter', methods=['POST'])
def add_article():
    titre = request.form['titre']
    contenu = request.form['contenu']
    auteur = request.form['auteur']
    categorie = request.form.get('categorie')
    tags = request.form.get('tags')

    new_article = Article(titre=titre, contenu=contenu, auteur=auteur,
                          categorie=categorie, tags=tags)
    db.session.add(new_article)
    db.session.commit()
    return redirect(url_for('show_articles'))

# Supprimer un article
@app.route('/articles-supprimer/<int:id>', methods=['POST'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('show_articles'))

# Modifier un article
@app.route('/articles-modifier/<int:id>', methods=['GET', 'POST'])
def edit_article(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.titre = request.form['titre']
        article.contenu = request.form['contenu']
        article.auteur = request.form['auteur']
        article.categorie = request.form.get('categorie')
        article.tags = request.form.get('tags')
        db.session.commit()
        return redirect(url_for('show_articles'))
    else:
        return render_template('edit_article.html', article=article)

if __name__ == "__main__":
    app.run(debug=True)