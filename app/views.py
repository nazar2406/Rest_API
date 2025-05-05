from flask import Flask, jsonify, request, abort
from marshmallow import Schema, fields, ValidationError
from . import app
import uuid

@app.route('/home')
def welcome():
    return "Вітаю!"

# 🔧 Обробка помилок
@app.errorhandler(404)
def handle_not_found(error):
    return jsonify(message=str(error)), 404

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify(message=str(error)), 400
