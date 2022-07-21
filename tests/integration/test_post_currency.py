from http import HTTPStatus

from flask.testing import FlaskClient
from pytest import mark


def test_register_function_route_201(
    client: FlaskClient, get_currency_payload, colorized
):
    """
    GIVEN the register currrency function
    WHEN I fetch a correct request
    THEN I receive the correct payload
    THEN I receive the status code 201
    """

    path = f"/api"
    payload = get_currency_payload()

    response = client.post(path, json=payload)

    assert response.content_type == "application/json", colorized(
        f"Verificar se a rota {path} foi configurada."
    )

    json: dict = response.json

    expected_keys = (
        "id",
        "code",
        "label",
        "is_crypto",
        "created_at",
        "updated_at",
    )

    assert set(json).issuperset(expected_keys)

    assert json["code"].lower() == payload["code"].lower()
    assert json["label"].lower() == payload["label"].lower()
    assert json["is_crypto"].lower() == payload["is_crypto"].lower()

    assert response.status_code == HTTPStatus.CREATED


@mark.parametrize("missed_field", ["code", "label", "is_crypto", "conversion"])
def test_register_function_route_missing_fields_400(
    client: FlaskClient, get_currency_payload, colorized, missed_field
):
    """
    GIVEN the register currrency function
    WHEN I fetch request missing required fields
    THEN I receive the correct error payload
    THEN I receive the status code 400
    """

    path = f"/api"
    payload: dict = get_currency_payload()

    payload.pop(missed_field)

    response = client.post(path, json=payload)

    assert response.content_type == "application/json", colorized(
        f"Verificar se a rota <{path}> foi configurada."
    )

    json: dict = response.json

    expected = {
        "error": "Validation error.",
        missed_field: ["Missing data for required field."],
    }

    assert set(json).issuperset(expected)

    for key, value in json.items():
        assert set(value).issuperset(expected[key])

    assert response.status_code == HTTPStatus.BAD_REQUEST


@mark.parametrize("obj_field", ["conversion"])
@mark.parametrize("missed_field", ["USD", "local"])
def test_register_function_route_missing_nested_fields_400(
    client: FlaskClient, get_currency_payload, colorized, obj_field, missed_field
):
    """
    GIVEN the register currrency function
    WHEN I fetch request missing required fields
    THEN I receive the correct error payload
    THEN I receive the status code 400
    """

    path = f"/api"
    payload: dict = get_currency_payload()

    payload[obj_field].pop(missed_field)

    response = client.post(path, json=payload)

    assert response.content_type == "application/json", colorized(
        f"Verificar se a rota <{path}> foi configurada."
    )

    json: dict = response.json

    expected = {
        "error": "Validation error.",
        missed_field: ["Missing data for required field."],
    }

    assert set(json).issuperset(expected)

    for key, value in json.items():
        assert set(value).issuperset(expected[key])

    assert response.status_code == HTTPStatus.BAD_REQUEST
