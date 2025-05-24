from flask import Blueprint, jsonify

# Створення Blueprint (можна підключити до app пізніше)
main_bp = Blueprint('main', __name__)

# Головна сторінка
@main_bp.route('/')
def home():
    return "Hello"

# Обробка помилки 404
@main_bp.app_errorhandler(404)
def handle_404(error):
    return jsonify({"error": str(error)}), 404

# Обробка помилки 400
@main_bp.app_errorhandler(400)
def handle_400(error):
    return jsonify({"error": str(error)}), 400
