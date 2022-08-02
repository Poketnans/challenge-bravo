from http import HTTPStatus

from flask import jsonify

from app.services import get_conversion_service


def get_conversion():
    payload = get_conversion_service()

    return jsonify(payload), HTTPStatus.OK
