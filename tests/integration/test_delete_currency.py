from http import HTTPStatus

from flask.testing import FlaskClient
from pytest import mark

from app.classes.app_with_db import AppWithDb
from app.models import Currency


@mark.parametrize("code", ["USD", "BRL", "EUR", "BTC", "ETH"])
def test_delete_restricted_currency_route_403(client: FlaskClient, code, colorized):
    """
    GIVEN the delete currrency route
    WHEN I try to delete a restricted currency
    THEN I received correct error message
    THEN I receive the status code 403
    """

    path = f"/api/{code}"

    response = client.delete(path)

    assert response.content_type == "application/json", colorized(
        f"Verificar se a rota <{path}> foi configurada."
    )

    json: dict = response.json

    expected = {
        "error": "This is a restricted currency. You can not delete it.",
    }

    assert json == expected, colorized(json)
    assert response.status_code == HTTPStatus.FORBIDDEN


@mark.parametrize("code", ["JPY", "EGP", "TRY", "COP", "RUB"])
def test_delete_not_registered_currency_route_404(client: FlaskClient, code, colorized):
    """
    GIVEN the delete currrency route
    WHEN I try to delete unregistered currency
    THEN I received correct error message
    THEN I receive the status code 404
    """

    path = f"/api/{code}"

    response = client.delete(path)

    assert response.content_type == "application/json", colorized(
        f"Verificar se a rota <{path}> foi configurada."
    )

    json: dict = response.json

    expected = {
        "error": "Currency not found.",
    }

    assert json == expected, colorized(json)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_currency_route_204(client: FlaskClient, new_currency, colorized):
    """
    GIVEN the delete currrency route
    WHEN I realise a correct request
    THEN I receive the status code 204
    """
    app: AppWithDb = client.application

    with app.app_context():
        path = f"/api/{new_currency.code}"

        response = client.delete(path)

        assert response.status_code == HTTPStatus.NO_CONTENT

        session = app.db.session
        query = session.query(Currency)
        currency_exists = bool(query.filter_by(code=new_currency.code).first())

        assert not currency_exists, colorized("O registro não foi deletado!")
