from datetime import datetime

from app.classes.app_with_db import current_app as curr_app
from app.services.create_or_update_service import create_or_update
from app.services.get_indirect_crypto_cotation_service import (
    get_indirect_crypto_cotation,
)
from app.services.get_indirect_internal_cotation import get_indirect_internal_cotation
from app.utils import fetch, get_quote_date, get_rate


def get_conversion_service():
    from_currency = curr_app.from_currency
    to_currency = curr_app.to_currency
    _from = from_currency.code
    to = to_currency.code
    amount = curr_app.amount_param
    conversion = 1
    quote_date = datetime.now()

    if _from == to:
        msg = {"message": "Nothing to convert."}
        return msg

    elif curr_app.cotation and (
        curr_app.cotation_is_updated
        or not from_currency.is_external
        or not to_currency.is_external
    ):
        cot_rate = curr_app.cotation.rate
        conversion = (
            amount / cot_rate if curr_app.inverted_conversion else amount * cot_rate
        )
        quote_date = curr_app.cotation.updated_at

    elif from_currency.is_crypto and not to_currency.backing_currency:
        cotation = get_indirect_crypto_cotation(from_currency, to_currency)
        conversion = amount * cotation.rate

    elif to_currency.is_crypto and not from_currency.backing_currency:
        cotation = get_indirect_crypto_cotation(to_currency, from_currency)
        conversion = amount / cotation.rate

    elif not from_currency.is_external:
        cotation = get_indirect_internal_cotation(from_currency, to_currency)
        conversion = amount * cotation.rate

    elif not to_currency.is_external:
        cotation = get_indirect_internal_cotation(to_currency, from_currency)
        conversion = amount / cotation.rate

    else:
        conversion_data = fetch(_from, to)
        quote_rate = float(get_rate(conversion_data))

        rate = (1 / quote_rate) if curr_app.inverted_conversion else quote_rate
        conversion = amount * rate

        cotation = create_or_update(
            from_currency,
            to_currency,
            rate,
            get_quote_date(conversion_data),
            curr_app.cotation,
        )

        quote_date = cotation.quote_date

    payload = {
        _from: round(amount, 4),
        to: round(conversion, 4),
        "quote_date": quote_date.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return payload
