from random import randrange

from flask import jsonify, request

from opinions_app import app, db
from opinions_app.models import Opinion
from opinions_app.views import random_opinion

"""
Сейчас функция привязана к модели Opinion и выполняет сериализацию данных только 
для объектов этой модели. В такой ситуации хорошим решением будет не оформлять сериализатор 
в отдельную функцию, а сделать его методом класса Opinion: это логично и позволит писать 
меньше кода в дальнейшем.
Удалите функцию opinion_to_dict() из файла api_views.py.
В модели Opinion опишите метод to_dict().
Теперь в функции get_opinion() не нужен вызов opinion_to_dict(), вместо этого для объекта модели 
нужно вызвать метод to_dict():
"""


# def opinion_to_dict(opinion):
#     """Преобразовать объект модели в словарь"""
#     return dict(
#         id=opinion.id,
#         title=opinion.title,
#         text=opinion.text,
#         source=opinion.source,
#         timestamp=opinion.timestamp,
#         added_by=opinion.added_by
#     )


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    """
    Получить отдельный объект модели по id или выбросить ошибку и
    конвертировать его в словарь.
    """
    # Получить объект по id или выбросить ошибку
    opinion = Opinion.query.get_or_404(id)
    # # Конвертируем объект модели в словарь
    # data = opinion_to_dict(opinion)
    # return jsonify({'opinion': data}), 200
    # Никаких лишних функций, просто метод to_dict():
    return jsonify({'opinion': opinion.to_dict()}), 200


# Обновление данных методом PATCH предполагает отправку одного или
# нескольких полей с новыми значениями в теле запроса.

# Задача сводится к следующему:
# разрешить для API-функции метод PATCH,
# получить id нужной записи из запроса к API,
# получить экземпляр модели из базы данных по id,
# получить новые значения полей из PATCH-запроса,
# изменить значения полей экземпляра модели на значения полей из запроса,
# зафиксировать изменения в базе данных,
# в ответ на запрос вернуть JSON с обновлённым объектом и соответствующий статус ответа.
# Параметры в теле PATCH-запроса передаются в формате JSON.
@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    """Обновить отдельный объект."""
    data = request.get_json()
    opinion = Opinion.query.get_or_404(id)
    # Если метод get_or_404 не найдёт указанный ключ,
    # то он выбросит исключение 404
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    # Все изменения нужно сохранить в базе данных
    db.session.commit()
    # При создании или изменении объекта вернём сам объект и код 201
    return jsonify({'opinion': opinion.to_dict()}), 201


# Удаление объекта: Delete

# Всё, что надо сделать — это:
# разрешить для функции метод DELETE,
# получить id объекта из DELETE- запроса,
# получить по id экземпляр модели из базы данных,
# выполнить ORM-запрос на удаление полученного объекта,
# зафиксировать изменения в базе данных,
# вернуть соответствующий код ответа.
@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    db.session.delete(opinion)
    db.session.commit()
    # При удалении принято возвращать только код ответа 204
    return '', 204


# Получение полного списка записей

# Спроектируем обработку запроса и подготовку ответа:
# при GET-запросе получить из базы данных все объекты модели Opinion,
# конвертировать объекты модели в словарь, а затем в JSON,
# вернуть JSON в ответ на GET-запрос.
@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    """Получить полный список записей."""
    # Запрашивается список объектов
    opinions = Opinion.query.all()
    # Поочерёдно сериализуется каждый объект,
    # а потом все объекты помещаются в список opinions_list
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    """Добавить новый объект."""
    # Получение данные из запроса в виде словаря
    data = request.get_json()
    # Создание нового пустого экземпляра модели
    opinion = Opinion()
    # Наполнение его данными из запроса
    opinion.from_dict(data)
    # Добавление новой записи в базу данных
    db.session.add(opinion)
    # Сохранение изменений
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


# Есть смысл создать отдельную функцию, которая будет выбирать случайный объект из модели,
# и тогда к этой функции можно будет обращаться из любого места программы.
# Добавьте в файл views.py функцию random_opinion() и обновите код index_view().

# Импортируйте функцию random_opinion() в api_views.py и обновите код get_random_opinion():
# @app.route('/api/get-random-opinion/', methods=['GET'])
# def get_random_opinion():
#     """Выбрать случайное мнение из базы данных."""
#     quantity = Opinion.query.count()
#     if quantity:
#         offset_value = randrange(quantity)
#         opinion = Opinion.query.offset(offset_value).first()
#         return jsonify({'opinion': opinion.to_dict()}), 200

@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    """Выбрать случайное мнение из базы данных."""
    opinion = random_opinion()
    return jsonify({'opinion': opinion.to_dict()}), 200
