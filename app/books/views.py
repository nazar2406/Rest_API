from flask import Blueprint, jsonify, request, abort
from marshmallow import Schema, fields
from app import db
from .models import Book

book_bp = Blueprint('book_bp', __name__)

# Схема для валідації та серіалізації
class BookSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    year = fields.Int(required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Отримати список книг з пагінацією
@book_bp.route('/', methods=['GET'])
def list_books():
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        abort(400, description="Invalid pagination parameters")

    books = Book.query.limit(limit).offset(offset).all()
    return jsonify(books_schema.dump(books)), 200

# Отримати одну книгу за ID
@book_bp.route('/<int:book_id>', methods=['GET'])
def retrieve_book(book_id):
    book = Book.query.get_or_404(book_id, description="Book not found")
    return jsonify(book_schema.dump(book)), 200

# Додати нову книгу
@book_bp.route('/add', methods=['POST'])
def create_book():
    json_data = request.get_json()
    if not json_data:
        abort(400, description="No input data provided")
    
    try:
        new_data = book_schema.load(json_data)
    except Exception as err:
        abort(400, description=f"Invalid data: {err}")

    new_book = Book(
        title=new_data['title'],
        author=new_data['author'],
        year=new_data['year']
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify(book_schema.dump(new_book)), 201

# Видалити книгу за ID
@book_bp.route('/delete/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    book = Book.query.get_or_404(book_id, description="Book not found")
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Book with ID {book_id} has been deleted."}), 200
