from http import HTTPStatus

from app.services import delete_currency_service


def delete_currency(code):
    delete_currency_service(code)

    return "", HTTPStatus.NO_CONTENT
