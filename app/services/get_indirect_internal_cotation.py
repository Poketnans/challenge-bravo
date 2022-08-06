from sqlalchemy.orm import Query

from app.classes.app_with_db import current_app as curr_app
from app.models import Cotation, Currency
from app.services.register_cotation import register_cotation
from app.services.update_cotation_service import update_cotation
from app.utils import check_cotation_is_updated, fetch, get_rate


def get_indirect_internal_cotation(
    internal: Currency, external: Currency
) -> tuple[float, str]:
    session = curr_app.db.session
    query: Query[Cotation] = session.query(Cotation)
    currency_query: Query[Currency] = session.query(Currency)

    usd_curr = currency_query.filter_by(code="USD").first()

    USD_to_internal_cotation = query.filter_by(code=f"USD{internal.code}").first()
    USD_to_internal_rate = (
        USD_to_internal_cotation.rate if USD_to_internal_cotation else 1
    )

    middle_cotation = query.filter_by(code=f"USD{external.code}").first()
    middle_cotation_rate = middle_cotation.rate if middle_cotation else 1
    middle_cotation_quote_date = (
        middle_cotation.quote_date.strftime("%Y-%m-%d %H:%M:%S")
        if middle_cotation
        else ""
    )

    if not middle_cotation or not check_cotation_is_updated(middle_cotation):
        middle_cotation_data = fetch("USD", external.code)
        middle_cotation_rate = float(get_rate(middle_cotation_data))
        middle_cotation_quote_date: str = middle_cotation_data["create_date"]

        if not middle_cotation:
            register_cotation(
                {
                    "rate": middle_cotation_rate,
                    "quote_date": middle_cotation_quote_date,
                    "from_currency": usd_curr,
                    "to_currency": external,
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

    cot_rate = USD_to_internal_rate / float(middle_cotation_rate)

    if not curr_app.cotation:
        register_cotation(
            {
                "rate": cot_rate,
                "quote_date": middle_cotation_quote_date,
                "from_currency": internal,
                "to_currency": external,
            }
        )

    if curr_app.cotation and not curr_app.cotation_is_updated:
        update_cotation(
            curr_app.cotation,
            {"rate": cot_rate, "quote_date": middle_cotation_quote_date},
        )

    return cot_rate, middle_cotation_quote_date
