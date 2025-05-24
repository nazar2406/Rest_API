from app import db


class Book(db.Model):
    # Визначаємо назву таблиці в базі даних
    __tablename__ = "books"

    # Оголошення колонок
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=120), nullable=False)
    author = db.Column(db.String(length=120), nullable=False)

    # Рядкове представлення моделі
    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}')"
