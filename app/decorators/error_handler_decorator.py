from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask import jsonify
from flask.wrappers import Response
from marshmallow.exceptions import ValidationError

from app.errors import CustomError


def error_handler(controller: Callable) -> Callable:
    """
    Handle the errors raised from descending decorators.
    The errors MUST be inrerited from `app.errors.CustomError`
    """

    @wraps(controller)
    def wrapper(*args, **kwargs) -> tuple[Response, int]:
        try:
            return controller(*args, **kwargs)
        except ValidationError as err:
            msg = {"error": "Validation error.", **err.messages}
            return jsonify(msg), HTTPStatus.BAD_REQUEST
        except CustomError as err:
            return jsonify(err.description), err.code

    return wrapper
