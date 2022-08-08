from datetime import datetime

from app.classes.app_with_db import current_app as curr_app
from app.services.get_indirect_crypto_cotation_service import (
    get_indirect_crypto_cotation,
)
from app.services.get_indirect_internal_cotation import get_indirect_internal_cotation
from app.services.register_cotation import register_cotation
from app.services.update_cotation_service import update_cotation
from app.utils import fetch


def get_conversion_service():
    from_currency = curr_app.from_currency
    to_currency = curr_app.to_currency
    _from = from_currency.code
    to = to_currency.code
    amount = curr_app.amount_param
    conversion = 1
    quote_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _from == to:
        msg = {"message": "Nothing to convert."}
        return msg

    elif curr_app.cotation and (
        curr_app.cotation_is_updated
        or not from_currency.is_external
        or not to_currency.is_external
    ):
        print(1)
        cot_rate = curr_app.cotation.rate
        conversion = (
            amount / cot_rate if curr_app.inverted_conversion else amount * cot_rate
        )
        quote_date = curr_app.cotation.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    elif from_currency.is_crypto and not to_currency.backing_currency:
        print(2)
        cotation = get_indirect_crypto_cotation(from_currency, to_currency)
        conversion = amount * cotation.rate

    elif to_currency.is_crypto and not from_currency.backing_currency:
        print(3)
        cotation = get_indirect_crypto_cotation(to_currency, from_currency)
        conversion = amount / cotation.rate

    elif not from_currency.is_external:
        cot_rate, quote_date = get_indirect_internal_cotation(
            from_currency, to_currency
        )
        conversion = amount * cot_rate

    elif not to_currency.is_external:
        cot_rate, quote_date = get_indirect_internal_cotation(
            to_currency, from_currency
        )
        conversion = amount / cot_rate

    else:
        print(4)
        conversion_data = fetch(_from, to)

        quote_date = conversion_data["create_date"]
        quote_rate = float(conversion_data.get("high", 1))

        rate = (1 / quote_rate) if curr_app.inverted_conversion else quote_rate
        conversion = amount * rate

        cotation = register_cotation(
            {
                "rate": rate,
                "quote_date": quote_date,
                "from_currency": from_currency,
                "to_currency": to_currency,
            }
        )

        quote_date = cotation.quote_date

    payload = {
        _from: round(amount, 4),
        to: round(conversion, 4),
        "quote_date": quote_date,
    }

    return payload
