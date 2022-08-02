from http import HTTPStatus

import requests

from app.classes.app_with_db import current_app


def fetch(_from: str, to: str = "USD") -> dict:
    BASE_URL = "https://economia.awesomeapi.com.br/last"
    url = f"{BASE_URL}/{_from}-{to}"
    response = requests.get(url)

    if response.status_code == HTTPStatus.NOT_FOUND:
        url = f"{BASE_URL}/{to}-{_from}"
        response = requests.get(url)
        current_app.inverted_conversion = True

    json = response.json()
    conversion_data = (
        json[f"{to.upper()}{_from.upper()}"]
        if current_app.inverted_conversion
        else json[f"{_from.upper()}{to.upper()}"]
    )
    return conversion_data
