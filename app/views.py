from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return "Hello"

@main_bp.app_errorhandler(404)
def handle_404(error):
    return jsonify({"error": str(error)}), 404

@main_bp.app_errorhandler(400)
def handle_400(error):
    return jsonify({"error": str(error)}), 400
