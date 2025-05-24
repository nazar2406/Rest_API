from flask import request, jsonify, abort
from marshmallow import Schema, fields
from . import book_bp
from .models import Book
from app import db

# 🔧 Marshmallow схема для серіалізації
class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# 📚 Отримання списку книг з курсорною пагінацією
@book_bp.route('/', methods=['GET'])
def list_books():
    limit = request.args.get('limit', default=10, type=int)
    after = request.args.get('after_id', type=int)
    before = request.args.get('before_id', type=int)

    query = Book.query.order_by(Book.id)

    if after is not None:
        query = query.filter(Book.id > after)
    elif before is not None:
        query = query.filter(Book.id < before).order_by(Book.id.desc())

    books = query.limit(limit).all()

    if before is not None:
        books.reverse()

    data = books_schema.dump(books)
    next_id = books[-1].id if books else None
    prev_id = books[0].id if books else None

    return jsonify({
        "books": data,
        "next_cursor": next_id,
        "prev_cursor": prev_id
    }), 200

# 🔍 Отримання конкретної книги
@book_bp.route('/<int:book_id>', methods=['GET'])
def retrieve_book(book_id):
    book = Book.query.get_or_404(book_id, description="Book not found")
    return book_schema.jsonify(book), 200

# ➕ Додавання нової книги
@book_bp.route('/add_book', methods=['POST'])
def create_book():
    json_data = request.get_json()
    if not json_data:
        abort(400, description="No input data provided")

    try:
        validated = book_schema.load(json_data)
    except Exception as e:
        abort(400, description=str(e))

    new_book = Book(**validated)
    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book), 201

# ❌ Видалення книги
@book_bp.route('/delete/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404, description="Book not found")

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200
