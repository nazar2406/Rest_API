from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Ініціалізація Flask-додатку
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Ініціалізація бази даних
    db.init_app(app)

    # Контекст додатку
    with app.app_context():
        # Імпорти всередині контексту, щоб уникнути циклічних імпортів
        from app.books.models import Book
        from app.books import book_bp  # Імпортуємо Blueprint
        from app import views          # Роутинг з views.py

        # Реєстрація Blueprint для книг
        app.register_blueprint(book_bp)

        # Створення таблиць у БД
        db.create_all()

    return app
