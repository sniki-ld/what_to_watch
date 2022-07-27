from flask import render_template

from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    """Обработать ошибку 404."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Обработать ошибку 500 и
    откатить незафиксированные изменения в БД.
    """
    db.session.rollback()
    return render_template('500.html'), 500