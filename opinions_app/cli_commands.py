import csv

import click

from . import app, db
from .models import Opinion


@app.cli.command('load_opinions')
def load_opinions_command():
    """Загрузить мнения в БД из файла csv."""
    with open('opinions.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений: {counter}')