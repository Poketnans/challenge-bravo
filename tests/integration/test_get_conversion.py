from datetime import datetime
from http import HTTPStatus
from random import randint

from flask.testing import FlaskClient
from pytest import mark

from app.classes.app_with_db import AppWithDb
from app.models import Currency


@mark.parametrize("from_currency", ["USD", "BRL", "EUR", "BTC", "ETH"])
@mark.parametrize("to_currency", ["USD", "BRL", "EUR"])
def test_get_conversion_200(
    client: FlaskClient,
    from_currency,
    to_currency,
    colorized,
):
    """
    GIVEN the rout '/api?from={cur1}&to={cur2}&amount={float}'
    WHEN I fetch a requisition
    THEN I get the status code 200
    THEN I get the correct payload response
    """

    if from_currency == to_currency:
        return

    path = "/api?from={_from}&to={to}&amount={amount}"

    # response format
    # {
    #   <from_currency>: <amount>,
    #   <to_currency>: float,
    #   "quote_date": "YYYY-MM-DD hh:mm:ss"
    # }
    expected_keys = lambda _from, to: (_from, to, "quote_date")
    expected_types = lambda _from, to: {
        _from: float,
        to: float,
        "quote_date": str,
    }

    path = path.format(
        _from=from_currency,
        to=to_currency,
        amount=randint(1, 10),
    )
    response = client.get(path)

    assert response.status_code == HTTPStatus.OK, colorized(
        f"Not able to convert {from_currency} to {to_currency}"
    )

    json: dict = response.json
    expected = expected_keys(from_currency, to_currency)
    assert set(json) == set(expected), colorized(
        f"{from_currency} - {to_currency} - {path}"
    )

    response_types = expected_types(from_currency, to_currency)

    assert type(json[from_currency]) == response_types[from_currency]
    assert type(json[to_currency]) == response_types[to_currency]
    assert datetime.strptime(json["quote_date"], "%Y-%m-%d %H:%M:%S")


@mark.parametrize("currency", ["USD", "BRL", "EUR", "BTC", "ETH"])
def test_get_conversion_passing_same_from_and_to_param(
    client: FlaskClient,
    currency,
    colorized,
):
    """
    GIVEN the conversion route
    WHEN I pass same currency to `from` and `to` param
    THEN I receive the correct message
    THEN I receive the status code 200
    """

    path = f"/api?from={currency}&to={currency}&amount=1"
    response = client.get(path)
    json: dict = response.json

    expected = {"message": "Nothing to convert."}

    assert json == expected
    assert response.status_code == HTTPStatus.OK


def test_get_conversion_unregistered_currency_404(
    client: FlaskClient, currency_codes, colorized
):
    """
    GIVEN the conversion route
    WHEN I inform non-registered currency
    THEN I receive the correct error message
    THEN I receive the status code 404
    """

    non_registered = "BRLT"

    path = f"/api?from={non_registered}&to=BRL&amount=5"

    expected = {
        "error": f"Currency {non_registered} not registered",
        "curencies": [*currency_codes],
    }

    response = client.get(path)

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert set(response.json).issuperset(expected), colorized(response)


@mark.parametrize(
    ("params", "missing"),
    [
        ("from=USD&to=BRL", ["amount"]),
        ("from=USD&amount=1", ["to"]),
        ("to=BRL&amount=1", ["from"]),
        ("from=USD", ["to", "amount"]),
        ("to=BRL", ["from", "amount"]),
        ("amount=1", ["from", "to"]),
        ("", ["from", "to", "amount"]),
    ],
)
def test_missing_query_params(client: FlaskClient, params, missing, colorized):
    """
    GIVEN the conversion route
    WHEN I do not inform necessary params
    THEN I received correct error message
    THEN I receive the status code 400
    """

    path = f"/api?{params}"

    missing_fields = {field: ["Missing param."] for field in missing}

    expected = {"error": "Validation error.", **missing_fields}

    response = client.get(path)

    assert set(response.json).issuperset(expected), colorized(response.json)

    for key, value in response.json.items():
        assert set(value).issuperset(expected[key]), colorized(response.json)

    assert response.status_code == HTTPStatus.BAD_REQUEST


@mark.parametrize("amount", ["abc", "USD"])
def test_wrong_amount_param_value_type(client, amount, colorized):
    """
    GIVEN the conversion route
    WHEN I pass wrong value types to `amount` param
    THEN I received correct error message
    THEN I receive the status code 400
    """

    path = f"/api?from=EUR&to=BRL&amount={amount}"

    expected = {
        "error": "Validation error.",
        "amount": ["Not a valid number."],
    }

    response = client.get(path)

    assert response.json == expected, colorized(response.json)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@mark.parametrize("_from", ["USD", "BRL", "EUR", "BTC", "ETH"])
@mark.parametrize("to", ["BTC", "ETH"])
def test_get_conversion_to_crypto_200(
    client: FlaskClient,
    _from,
    to,
    colorized,
):
    """
    GIVEN the conversion route
    WHEN I try to convert any currency to cripto-currency
    THEN I received correct response
    THEN I receive the status code 200
    """

    if _from == to:
        return

    path = f"/api?from={_from}&to={to}&amount={randint(1, 10)}"

    expected_keys = lambda _from, to: (_from, to, "quote_date")
    expected_types = lambda _from, to: {
        _from: float,
        to: float,
        "quote_date": str,
    }

    response = client.get(path)

    assert response.content_type == "application/json", colorized(
        f"Verificar se a rota <{path}> foi configurada."
    )

    assert response.status_code == HTTPStatus.OK, colorized(
        f"Not able to convert {_from} to {to}"
    )

    json: dict = response.json
    expected = expected_keys(_from, to)
    assert set(json) == set(expected), colorized(f"{_from} - {to} - {path}")

    response_types = expected_types(_from, to)

    assert type(json[_from]) == response_types[_from]
    assert type(json[to]) == response_types[to]
    assert datetime.strptime(json["quote_date"], "%Y-%m-%d %H:%M:%S")


@mark.parametrize("external", ["USD", "BRL", "EUR", "BTC", "ETH"])
def test_get_conversion_internal_to_external_crypto_200(
    client: FlaskClient, external, colorized, get_currency_payload
):
    """
    GIVEN the created currencies called `internal`
    GIVEN the initial currencies called `external`
    GIVEN the conversion route
    WHEN I try to convert any external to internal
    THEN I received correct response
    THEN I receive the status code 200
    """

    baseUrl = "/api"

    payload = get_currency_payload()

    response = client.post(baseUrl, json=payload)

    assert response.content_type == "application/json", colorized(
        f"Não deu certo criar a moeda {payload['code']}."
    )

    new_currency: dict = response.json

    internal = new_currency["code"]

    path = (
        f"{baseUrl}?from={new_currency['code']}&to={external}&amount={randint(1, 10)}"
    )

    expected_keys = lambda _from, to: (_from, to, "quote_date")
    expected_types = lambda _from, to: {
        _from: float,
        to: float,
        "quote_date": str,
    }

    response = client.get(path)

    assert response.content_type == "application/json", colorized(
        f"Verificar se a rota <{path}> foi configurada."
    )

    assert response.status_code == HTTPStatus.OK, colorized(
        f"Not able to convert {internal} to {external}"
    )

    json: dict = response.json
    expected = expected_keys(internal, external)
    assert set(json) == set(expected), colorized(f"{internal} - {external} - {path}")

    response_types = expected_types(internal, external)

    assert type(json[internal]) == response_types[internal]
    assert type(json[external]) == response_types[external]
    assert datetime.strptime(json["quote_date"], "%Y-%m-%d %H:%M:%S")
