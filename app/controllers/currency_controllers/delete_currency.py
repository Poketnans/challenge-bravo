from app.classes.app_with_db import current_app
from app.errors import CurrencyNotFoundError, InitialCurrencyForbiddenError
from app.models import Currency
from app.services import filter_by_or_404
from app.utils import get_initial_currencies


def delete_currency(code):

    session = current_app.db.session
    query = session.query(Currency)

    initial_currencies_codes = [
        currency["code"] for currency in get_initial_currencies()
    ]

    if code in initial_currencies_codes:
        raise InitialCurrencyForbiddenError

    currency = filter_by_or_404(query, {"code": code}, exception=CurrencyNotFoundError)

    session.delete(currency)
    session.commit()

    return "", 204
