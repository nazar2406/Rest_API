from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # Ініціалізація Flask-додатку
    app = Flask(__name__)

    # Завантаження конфігурації з об'єкта
    app.config.from_object("config.Config")

    # Ініціалізація бази даних
    db.init_app(app)

    # Реєстрація blueprint'ів і створення таблиць
    with app.app_context():
        # Імпорти всередині контексту для уникнення циклічних залежностей
        from app.books.models import Book
        from app.books import views  # Якщо є view-функції в цьому модулі
        from app.books import book_bp

        app.register_blueprint(book_bp)

        # Створення таблиць (якщо вони ще не існують)
        db.create_all()

    return app
