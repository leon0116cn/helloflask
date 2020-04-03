import click
from watchlist import app, db
from watchlist.models import User, Movie


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

    for movie in movies:
        db.session.add(Movie(**movie))
    
    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option(
    '--password', prompt=True, hide_input=True, confirmation_prompt=True, 
    help='The password used to login.'
)
def admin(username, password):
    '''创建admin账户'''
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(name='Admin', username=username)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')