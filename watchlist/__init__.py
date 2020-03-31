import os
import sys
import click
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(
    os.path.dirname(app.root_path), 'data.db'
    )
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    movies = db.session.query(Movie).all()
    return render_template('index.html', movies=movies)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    '''Initialize the database.'''
    if drop:
        db.drop_all()
        click.echo('Droped the database.')
    db.create_all()
    click.echo('Initialized the database.')


@app.cli.command()
def forge():
    '''Generate fake data.'''
    db.create_all()

    name = 'Leon Lv'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    db.session.add(User(name=name))
    for movie in movies:
        db.session.add(Movie(**movie))
    
    db.session.commit()
    click.echo('Done.')


@app.context_processor
def inject_user():
    user = db.session.query(User).first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    user = db.session.query(User).first()
    return render_template('404.html'), 404


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<User(id={}, name={})>'.format(self.id, self.name)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4))

    def __repr__(self):
        return '<Movie(id={}, title={}, year={})>'.format(
            self.id, self.title, self.year
            )
