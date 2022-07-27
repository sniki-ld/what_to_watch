"""
Здесь начало работы с Flask:
 - Каркас для сайта
 - Конфигурация приложения
 - Подключение базы данных. SQLAlchemy
 - Описание моделей и работа с БД
 - Шаблонизатор
 - Формирование ссылок из шаблона
 - Динамические адреса и конвертеры пути
 - Формы во Flask
 """

# from datetime import datetime
#
# # Импортируется функция выбора случайного значения
# from random import randrange
#
# # Обновите импорты из модуля Flask. Добавились функции redirect и url_for
# from flask import Flask, redirect, render_template, url_for
#
# # Как подключить БД к проекту
# # Импортируется нужный класс
# from flask_sqlalchemy import SQLAlchemy
#
# # Новые импорты для формы
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, TextAreaField, URLField
# from wtforms.validators import DataRequired, Length, Optional
#
# # Здесь создаётся объект приложения как экземпляр класса`Flask`,
# # который импортируется из модуля `flask`.
# # Единственный обязательный аргумент при создании экземпляра класса —
# # это имя текущего модуля или пакета приложения.
# app = Flask(__name__)
#
# # Подключается БД SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# # по умолчанию ORM отслеживает изменение моделей.
# # Эта операция забирает много ресурсов, и разработчики рекомендуют явным образом определять
# # необходимость её использования. Если функция нужна, то конфигурационному ключу
# # SQLALCHEMY_TRACK_MODIFICATIONS присваивается значение True, если нет — False.
# # Задаётся конкретное значение для конфигурационного ключа
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # Для корректной работы с формами в настройках проекта необходимо
# # указать значение ключа SECRET_KEY.
# # Его значение — строка из случайного набора символов.
# app.config['SECRET_KEY'] = 'MY SECRET KEY for project'
#
# # Создаётся экземпляр класса SQLAlchemy и передаётся
# # в качестве параметра экземпляр приложения Flask
# db = SQLAlchemy(app)
#
#
# class Opinion(db.Model):
#     """Модель для работы с мнениями."""
#     # ID — целое число, первичный ключ
#     id = db.Column(db.Integer, primary_key=True)
#     # Название фильма — строка длиной 128 символов, не может быть пустым
#     title = db.Column(db.String(128), nullable=False)
#     # Мнение о фильме — большая строка, не может быть пустым,
#     # должно быть уникальным
#     text = db.Column(db.Text, unique=True, nullable=False)
#     # Ссылка на сторонний источник — строка длиной 256 символов
#     source = db.Column(db.String(256))
#     # Дата и время — текущее время,
#     # по этому столбцу база данных будет проиндексирована
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#
#
# # Поля id и timestamp заполняются автоматически при сохранении информации в базу данных.
# # Значит, чтобы пользователь мог добавить на сайт собственное мнение о фильме,
# # нужно предоставить ему возможность заполнить следующие поля:
# # title — название фильма, обязательно;
# # source — ссылка на сторонний источник, необязательно;
# # text — мнение о фильме, обязательно.
# # Таким образом, форма для добавления нового мнения должна состоять из трёх полей.
# # Также на странице с формой должна быть кнопка «Добавить», нажав которую пользователь
# # отправит своё мнение о фильме в базу данных, и оно станет доступным для других пользователей.
# # Саму форму можно описать обычным Python-классом, который должен быть унаследован от
# # базового класса Flaskform модуля Flask-WTF. Типы полей формы и валидаторы должны
# # быть импортированы из библиотеки WTForms.
# # Класс формы опишите сразу после модели Opinion
# class OpinionForm(FlaskForm):
#     """Форма для мнения"""
#     title = StringField(
#         'Введите название фильма',
#         validators=[DataRequired(message='Обязательное поле'),
#                     Length(1, 128)]
#     )
#     text = TextAreaField(
#         'Напишите мнение',
#         validators=[DataRequired(message='Обязательное поле')]
#     )
#     source = URLField(
#         'Добавьте ссылку на подробный обзор фильма',
#         validators=[Length(1, 256), Optional()]
#     )
#     submit = SubmitField('Добавить')
#
#
# # @app.route('/')
# # def index_view():
# #     # Настройки хранятся в глобальном объекте config.
# #     # Доступ к нему можно получить через атрибут config экземпляра приложения app.
# #     # Глобальный объект config можно рассматривать и использовать как обычный словарь Python,
# #     # применяя к нему методы, которые обычно используются со словарями.
# #     # Чтобы посмотреть, какие настройки уже содержит проект, можно временно вывести
# #     # содержимое объекта config в терминал.
# #     # Добавьте в функцию index_view() инструкцию print(app.config):
# #     # print(app.config)
# #     return 'Совсем скоро тут будет случайное мнение о фильме!'
#
# """Первое, что должен увидеть пользователь проекта, с которым вы работаете —
# страницу с мнением о случайном фильме. Содержимое этой страницы формируется
# функцией index_view(). Именно в ней нужно получать то самое случайное мнение из базы данных.
# Узнать, сколько мнений есть в базе данных.
# Если их нет, сообщить об этом на странице и закончить работу функции.
# Иначе сгенерировать случайное число в диапазоне от нуля до числа равного количеству мнений в базе данных.
# В общем списке мнений пропустить то количество объектов, которое равно полученному случайному значению.
# В качестве результата выбрать следующий объект.
# Например, нужно выбрать случайное мнение из базы данных, в которой есть десять объектов.
# Первым делом нужно сгенерировать случайное число от нуля до девяти включительно.
# Пусть это будет число три. Первые три объекта в списке будут пропущены и выберется следующий —
# четвёртый. То есть, привязки к значению ID объекта в этом варианте не будет,
# ориентиром станет позиция объекта в списке.
# """
#
#
# @app.route('/')
# def index_view():
#     """Выбрать случайное мнение из базы данных"""
#     # Определяется количество мнений в базе данных
#     quantity = Opinion.query.count()
#     # Если мнений нет,
#     if not quantity:
#         # то возвращается сообщение
#         return 'В базе данных мнений о фильмах нет.'
#     # Иначе выбирается случайное число в диапазоне от 0 и до quantity
#     offset_value = randrange(quantity)
#     # И определяется случайный объект
#     opinion = Opinion.query.offset(offset_value).first()
#     # return opinion.text
#     # Рендеринг шаблонов во Flask осуществляется с помощью функции render_template().
#     # Эта функция принимает имя шаблона как обязательный аргумент и переменные контекста
#     # как дополнительные аргументы.
#     # Функция index_view() получает из базы данных объект класса Opinion
#     # Вам понадобится почти всё из этого списка, поэтому в шаблон лучше передавать
#     # не отдельные значения полей, а сразу весь объект.
#     # Вот здесь в шаблон передаётся весь объект opinion
#     # return render_template('index.html', opinion=opinion)
#     # Обновите имена шаблонов у функций index_view и add_opinion_view после рефакторинга шаблонов
#     # Тут подключается новый шаблон
#     return render_template('opinion.html', opinion=opinion)
#
#
# # GET-запрос разрешён по умолчанию, осталось для функции add_opinion_view() разрешить ещё и
# # POST-запрос. Это позволяет сделать декоратор @app.route.
# @app.route('/add', methods=['GET', 'POST'])
# def add_opinion_view():
#     """Добавить мнение о фильме"""
#     # # return 'Страница в разработке!'
#     # # И тут тоже
#     # return render_template('add_opinion.html')
#     # Класс формы описан. Теперь можно создать экземпляр этого класса и
#     # передать его в шаблон для отрисовки.
#     # Вот тут создаётся новый экземпляр формы
#     form = OpinionForm()
#     # Для обработки POST-запроса воспользуйтесь методом экземпляра формы validate_on_submit().
#     # Он запускает все необходимые проверки, и если всё проходит успешно —
#     # возвращает в качестве ответа True.
#     # Если ошибок не возникло, то
#     if form.validate_on_submit():
#         # нужно создать новый экземпляр класса Opinion
#         opinion = Opinion(
#             title=form.title.data,
#             text=form.text.data,
#             source=form.source.data
#         )
#         # Затем добавить его в сессию работы с базой данных
#         db.session.add(opinion)
#         # И зафиксировать изменения
#         db.session.commit()
#         # В случае успешного создания новой записи, пользователя нужно переадресовать на
#         # страницу добавленного мнения. С этим справится функция redirect из пакета Flask.
#         # При вызове функции достаточно в качестве параметра указать URL-адрес,
#         # на который нужно перейти. Адрес можно указать явно, но хорошей практикой будет
#         # использование функции url_for().
#         # Затем перейти на страницу добавленного мнения
#         return redirect(url_for('opinion_view', id=opinion.id))
#     # Иначе просто отрисовать страницу с формой
#     return render_template('add_opinion.html', form=form)
#
#
# # Тут указывается конвертер пути для id
# @app.route('/opinions/<int:id>')
# # Параметром указывается имя переменной
# def opinion_view(id):
#     """Формирует отдельную страницу мнения с конкретным ID. """
#     # Теперь можно запрашивать мнение по id
#     # opinion = Opinion.query.get(id)
#     # Чтобы избежать ошибки если нет такого id, можно заменить метод get на метод get_or_404():
#     # Метод get заменён на метод get_or_404()
#     opinion = Opinion.query.get_or_404(id)
#     # И передавать его в шаблон
#     return render_template('opinion.html', opinion=opinion)
#
#
# if __name__ == '__main__':
#     app.run()

"""
Здесь весь предыдущий код и добавляется:
 - Отправка флеш-сообщений
 - Кастомные страницы ошибок
 - Работа с миграциями
 - Пользовательские команды Flask
 """

from datetime import datetime
from random import randrange

# модуль для работы с файлами в формате csv
import csv
# модуль для создания пользовательских команд
import click

# Импортируйте функцию flash, abort из модуля flask
from flask import Flask, redirect, render_template, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional
# Импортируйте класс Migrate
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY SECRET KEY'

db = SQLAlchemy(app)
# Создайте экземпляр класса Migrate, передав в качестве параметров
# созданные ранее экземпляр приложения и экземпляр базы данных.
migrate = Migrate(app, db)


class Opinion(db.Model):
    """Модель для работы с мнениями."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Новое поле
    added_by = db.Column(db.String(64))


class OpinionForm(FlaskForm):
    """Форма для мнения"""
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    text = TextAreaField(
        'Напишите мнение',
        validators=[DataRequired(message='Обязательное поле')]
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1, 256), Optional()]
    )
    submit = SubmitField('Добавить')


# Зарегистрировать функцию-обработчик во Flask можно
# указав перед ней декоратор @app.errorhandler().
# новую функцию с именем page_not_found — она будет обрабатывать исключение
# «404: страница не найдена»:
# Тут декорируется обработчик и указывается код нужной ошибки
@app.errorhandler(404)
def page_not_found(error):
    """Обработать исключение 404"""
    # В качестве ответа возвращается собственный шаблон
    # и код ошибки
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработать исключение 500."""
    # В таких случаях можно откатить незафиксированные изменения в БД
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
def index_view():
    """Выбрать случайное мнение из базы данных"""
    quantity = Opinion.query.count()
    if not quantity:
        # Заменить это на abort(404)
        # return 'В базе данных записей нет.'
        abort(404)
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    """Добавить мнение о фильме"""
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        # Если в БД уже есть мнение с текстом, который ввёл пользователь,
        if Opinion.query.filter_by(text=text).first() is not None:
            # вызвать функцию flash и передать соответствующее сообщение
            flash('Такое мнение уже было оставлено ранее!')
            # и вернуть пользователя на страницу «Добавить новое мнение»
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id):
    """Формирует отдельную страницу мнения с конкретным ID."""
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)


# Чтобы создать собственную команду для приложения на Flask, нужно описать
# соответствующую функцию в коде проекта
# и применить к ней декоратор @app.cli.command().
# Декоратор @app.cli.command() первым аргументом принимает строку,
# которая используется как имя команды. Если имя не задано, оно генерируется из названия функции.
# Задача будущей команды и связанной с ней функции — построчно читать файл opinions.csv
# и добавлять прочитанные мнения в базу данных проекта через ORM.
@app.cli.command('load_opinions')
def load_opinions_command():
    """Функция загрузки мнений в базу данных."""
    # Открывается файл
    with open('../opinions.csv', encoding='utf-8') as f:
        # Создаётся итерируемый объект, который отображает каждую строку
        # в качестве словаря с ключами из шапки файла
        reader = csv.DictReader(f)
        # Для подсчёта строк добавляется счётчик
        counter = 0
        for row in reader:
            # Распакованный словарь можно использовать
            # для создания объекта мнения
            opinion = Opinion(**row)
            # Изменения нужно зафиксировать
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений: {counter}')


if __name__ == '__main__':
    app.run()
