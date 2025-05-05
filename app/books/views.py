from flask import Flask, jsonify, request, abort
from marshmallow import Schema, fields, ValidationError
import uuid
from . import book_bp

class BookDTO(Schema):
    uid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    writer = fields.Str(required=True)
    published = fields.Int(required=True)

book_dto = BookDTO()
book_list_dto = BookDTO(many=True)

library = [
    {
        "uid": 1,
        "name": "1984",
        "writer": "George Orwell",
        "published": 1949
    },
    {
        "uid": 2,
        "name": "Brave New World",
        "writer": "Aldous Huxley",
        "published": 1932
    },
    {
        "uid": 3,
        "name": "Fahrenheit 451",
        "writer": "Ray Bradbury",
        "published": 1953
    }
]

@book_bp.route('/all', methods=['GET'])
def fetch_all_books():
    return jsonify(library), 200

@book_bp.route('/book/<int:uid>', methods=['GET'])
def fetch_single_book(uid):
    selected = next((item for item in library if item["uid"] == uid), None)
    if not selected:
        abort(404, description="Книгу не знайдено")
    return jsonify(selected), 200

@book_bp.route('/create', methods=['POST'])
def create_book():
    try:
        payload = book_dto.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    payload["uid"] = str(uuid.uuid4())  # Генеруємо новий UUID
    library.append(payload)
    return jsonify(payload), 201

@book_bp.route('/remove/<string:uid>', methods=['DELETE'])
def remove_book(uid):
    global library
    item = next((b for b in library if b["uid"] == uid), None)
    if not item:
        abort(404, description="Книгу не знайдено")

    library = [b for b in library if b["uid"] != uid]
    return jsonify({"message": "Книгу успішно видалено"}), 200
