from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from werkzeug.exceptions import NotFound

from blog.database import db
from blog.forms.article import CreateArticleForm
from blog.mymodels import Article, Author

article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../static')

ARTICLES = {
    1: {
        'title': 'Ruslan and Ludmila',
        'text': '1 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin mollis urna eu malesuada commodo. Suspendisse lacinia, velit vitae mattis ',
        'author': 1,
    },
    2: {
        'title': 'Borodino',
        'text': '2 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin mollis urna eu malesuada commodo. Suspendisse lacinia, velit vitae mattis ',
        'author': 2,
    },
    3: {
        'title': 'War and Peace',
        'text': '3 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin mollis urna eu malesuada commodo. Suspendisse lacinia, velit vitae mattis ',
        'author': 3,
    }
}


@article.route('/', methods=["GET"])
def article_list():
    articles = Article.query.all()
    return render_template('articles/list.html', articles=articles)


@article.route('/<int:pk>')
def get_article(pk: int):
    try:
        _article = Article.query.filter_by(id=pk).one_or_none()
    except KeyError:
        raise NotFound(f'Article id {pk} not found')
    return render_template(
        'articles/details.html',
        article_name=_article
    )


@article.route('/create/', methods=['GET'])
def create_article_form():
    form = CreateArticleForm(request.form)
    return render_template('articles/create.html', form=form)


@article.route('/', methods=['POST'])
def create_article():
    form = CreateArticleForm(request.form)
    if form.validate_on_submit():
        _article = Article(title=form.title.data.strip(), text=form.text.data)
        if current_user.author:
            _article.author_id = current_user.author.id
        else:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            _article.author_id = author.id

        db.session.add(_article)
        db.session.commit()

        return redirect(url_for('article.article_detail', article_id=_article.id))

    return render_template('articles/create.html', form=form)
