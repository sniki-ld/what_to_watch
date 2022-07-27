from datetime import datetime

from . import db


class Opinion(db.Model):
    """Модель для работы с мнениями."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))

    # сериализатор
    def to_dict(self):
        """Преобразовать объект модели в словарь. Сериализатор."""
        return dict(
            id=self.id,
            title=self.title,
            text=self.text,
            source=self.source,
            timestamp=self.timestamp,
            added_by=self.added_by
        )

    # Для добавления нового объекта нужно описать десериализатор,
    # сделаем его методом модели Opinion;
    # назовём его from_dict(). Его задачей будет добавлять в пустой объект класса
    # Opinion значения полей, которые получены в POST-запросе.
    # Выполнить эту операцию можно при помощи функции setattr():
    # она добавляет объекту заданный атрибут.
    # В новый метод нужно передать значения полей
    # title, text, source, added_by,
    # которые и будут присвоены соответствующим полям нового объекта.
    # Поля id и timestamp создадутся автоматически при сохранении объекта в базе данных.

    # Добавляем в модель метод-десериализатор.
    # На вход метод принимает словарь data, полученный из JSON в запросе
    def from_dict(self, data):
        """Создать и сохранить новый объект модели Opinion. Десериализатор"""
        # Для каждого поля модели, которое можно заполнить...
        for field in ['title', 'text', 'source', 'added_by']:
            # ...выполняется проверка: есть ли ключ с таким же именем в словаре
            if field in data:
                # Если есть — добавляем значение из словаря
                # в соответствующее поле объекта модели:
                setattr(self, field, data[field])