from datetime import datetime

from sqlalchemy.orm import Query

from app.classes.app_with_db import current_app as curr_app
from app.models import Cotation, Currency
from app.services.register_cotation import register_cotation
from app.utils import fetch, get_crypto_rate, get_rate


def get_cotation_info(
    from_currency: Currency, to_currency: Currency
) -> tuple[float, str]:
    _from = from_currency.code
    to = to_currency.code
    session = curr_app.db.session
    query: Query[Cotation] = session.query(Cotation)

    usd_curr = session.query(Currency).filter_by(code="USD").first()

    crypto_to_USD = query.filter_by(code=f"{_from}USD").first()
    cot_rate = crypto_to_USD.rate if crypto_to_USD else 1
    quote_date = (
        crypto_to_USD.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        if crypto_to_USD
        else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    if not crypto_to_USD:
        crypto_to_USD = fetch(_from)
        cot_rate = get_crypto_rate(get_rate(crypto_to_USD))
        quote_date: str = crypto_to_USD["create_date"]

        register_cotation(cot_rate, quote_date, from_currency, usd_curr)

    if not to_currency.backing_currency:
        middle_cotation = query.filter_by(code=f"USD{to}").first()
        middle_cot_rate = middle_cotation.rate if middle_cotation else 1
        if not middle_cotation:
            middle_cotation = query.filter_by(code=f"{to}USD").first()
            middle_cot_rate = 1 / middle_cotation.rate if middle_cotation else 1
        if not middle_cotation:
            middle_cotation = fetch("USD", to)
            middle_cot_rate = get_rate(middle_cotation)

            register_cotation(middle_cot_rate, quote_date, usd_curr, to_currency)

        cot_rate = cot_rate * float(middle_cot_rate)
    register_cotation(cot_rate, quote_date, from_currency, to_currency)
    return cot_rate, quote_date
