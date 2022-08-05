from environs import Env

from app.models.currencies_model import Currency
from tests.utils import gen_unique

Env().read_env()

import os
from typing import Callable

import flask_migrate as fm
from colorama import Fore
from faker import Faker
from pytest import fixture

from app import create_app
from app.classes.app_with_db import AppWithDb


@fixture
def app():
    """Cria e configura uma nova aplicação para cada teste usando um banco de
    teste temporário aplciando as migrações. Antes de cada teste, deleta o banco
    existente"""
    os.environ["FLASK_ENV"] = "test"

    app = create_app()

    db_path = os.getenv("DB_TEST_PATH", "db_test.sqlite3")

    with app.app_context():
        if os.path.exists(f"app/{db_path}"):
            os.remove(f"app/{db_path}")
        fm.upgrade()

    yield app


@fixture
def client(app: AppWithDb):
    """Um client Test da aplicação"""
    return app.test_client()


@fixture
def colorized() -> Callable[[str], str]:
    """Retorna uma função anônima que adiciona informações de cor a uma\n
    string para melhor visualização no terminal. Retorna a seguinte função::

        colorized(msg: str) -> str

    Exemplo::

        def test_if_get_route_returns_correct_status_code(colorized):

            resp = requests.get(...)

            err_msg = "Status code errado!"

            assert resp.status_code == 200, colorized(err_msg)"""
    return lambda msg: f"{Fore.CYAN}{msg}{Fore.RESET}"


@fixture
def fake() -> Faker:
    """Retorna uma instância do objeto `faker.Faker`

    Exemplo::

        def test_if_create_route_returns_correct_status_code(fake):
            payload = {
                "name": fake.name(),
                "email": fake.email(),
                "password": fake.password(),
                "description": fake.text(),
            }

            resp = post("/users", payload)

            err_msg = "Status code errado!"

            assert resp.status_code == 201, err_msg"""
    return Faker()


@fixture
def get_currency_data(fake, currency_codes, currency_labels):

    return lambda: {
        "code": gen_unique(currency_codes, fake.currency_code),
        "label": gen_unique(currency_labels, fake.currency_name),
    }


@fixture
def get_currencies(fake, currency_codes, currency_labels, get_currency_data):

    curr_1 = Currency(**get_currency_data())

    codes = [*currency_codes, curr_1.code]
    labels = [*currency_labels, curr_1.label]

    curr_2_data = {
        "code": gen_unique(codes, fake.currency_code),
        "label": gen_unique(labels, fake.currency_name),
    }

    curr_2 = Currency(**curr_2_data)
    return lambda: (curr_1, curr_2)


@fixture
def get_cotation_data(fake):

    return lambda curr1, curr2: {
        "code": f"{curr1.code}-{curr2.code}",
        "rate": float(f"{fake.random.randint(0,99)}.{fake.random.randint(11,99)}"),
        "quote_date": fake.date_time(),
    }


@fixture
def currency_codes():
    return (
        "USD",
        "BRL",
        "EUR",
        "BTC",
        "ETH",
    )


@fixture
def currency_labels():
    return (
        "Dólar Americano",
        "Real Brasileiro",
        "Euro",
        "Bitcoin",
        "Ethereum",
    )


@fixture
def get_currency_payload(fake, currency_codes, currency_labels):
    """
    Gera informações aleatórias para a requisição de registro de moedas.
    As moedas são diferentes das moedas padrão.
    """

    def gen_payload(fake):
        return {
            "code": gen_unique(currency_codes, fake.currency_code),
            "label": gen_unique(currency_labels, fake.currency_name),
            "is_crypto": False,
            "conversion": {
                "USD": float(
                    f"{fake.random.randint(0,99)}.{fake.random.randint(11,99)}"
                ),
                "local": float(
                    f"{fake.random.randint(0,99)}.{fake.random.randint(11,99)}"
                ),
            },
        }

    return lambda: gen_payload(fake)


@fixture
def new_currency(get_currency_data, app: AppWithDb):
    with app.app_context():
        session = app.db.session

        currency = Currency(**get_currency_data())

        session.add(currency)
        session.commit()

        yield currency
