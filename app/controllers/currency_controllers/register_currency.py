from http import HTTPStatus

from flask import jsonify

from app.services import register_currency_service


def register_currency():
    new_currency = register_currency_service()

    return jsonify(new_currency), HTTPStatus.CREATED
