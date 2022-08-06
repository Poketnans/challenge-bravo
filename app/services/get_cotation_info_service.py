from sqlalchemy.orm import Query

from app.classes.app_with_db import current_app as curr_app
from app.models import Cotation, Currency
from app.services.register_cotation import register_cotation
from app.services.update_cotation_service import update_cotation
from app.utils import check_cotation_is_updated, fetch, get_crypto_rate, get_rate


def get_cotation_info(crypto: Currency, currency: Currency) -> tuple[float, str]:
    session = curr_app.db.session
    query: Query[Cotation] = session.query(Cotation)
    currency_query: Query[Currency] = session.query(Currency)

    usd_curr = currency_query.filter_by(code="USD").first()

    cot_crypto_to_USD = query.filter_by(code=f"{crypto.code}USD").first()
    crypto_to_USD_rate = cot_crypto_to_USD.rate if cot_crypto_to_USD else 1
    crypto_to_USD_quote_date = (
        cot_crypto_to_USD.quote_date.strftime("%Y-%m-%d %H:%M:%S")
        if cot_crypto_to_USD
        else ""
    )

    if not cot_crypto_to_USD:
        crypto_to_USD_data = fetch(crypto.code)
        crypto_to_USD_rate = get_crypto_rate(get_rate(crypto_to_USD_data))
        crypto_to_USD_quote_date: str = crypto_to_USD_data["create_date"]

        register_cotation(
            {
                "rate": crypto_to_USD_rate,
                "quote_date": crypto_to_USD_quote_date,
                "from_currency": crypto,
                "to_currency": usd_curr,
            }
        )

    middle_cotation = query.filter_by(code=f"USD{currency.code}").first()
    middle_cotation_rate = middle_cotation.rate if middle_cotation else 1
    middle_cotation_quote_date = (
        cot_crypto_to_USD.quote_date.strftime("%Y-%m-%d %H:%M:%S")
        if cot_crypto_to_USD
        else ""
    )

    # if not middle_cotation or not check_cotation_is_updated(middle_cotation):
    #     middle_cotation = query.filter_by(code=f"{currency.code}USD").first()
    #     middle_cotation_rate = 1 / middle_cotation.rate if middle_cotation else 1

    if not middle_cotation or not check_cotation_is_updated(middle_cotation):
        middle_cotation_data = fetch("USD", currency.code)
        middle_cotation_rate = float(get_rate(middle_cotation_data))
        middle_cotation_quote_date: str = middle_cotation_data["create_date"]

        if not middle_cotation:
            register_cotation(
                {
                    "rate": 1 / middle_cotation_rate,
                    "quote_date": middle_cotation_quote_date,
                    "from_currency": currency,
                    "to_currency": usd_curr,
                }
            )

        elif not check_cotation_is_updated(middle_cotation):
            update_cotation(
                middle_cotation,
                {
                    "rate": middle_cotation_rate,
                    "quote_date": middle_cotation_quote_date,
                },
            )

    cot_rate = crypto_to_USD_rate * float(middle_cotation_rate)

    if not curr_app.cotation:
        register_cotation(
            {
                "rate": cot_rate,
                "quote_date": middle_cotation_quote_date,
                "from_currency": crypto,
                "to_currency": currency,
            }
        )

    if curr_app.cotation and not curr_app.cotation_is_updated:
        update_cotation(
            curr_app.cotation,
            {"rate": cot_rate, "quote_date": middle_cotation_quote_date},
        )

    return cot_rate, middle_cotation_quote_date
