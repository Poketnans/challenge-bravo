from datetime import datetime

from app.classes.app_with_db import current_app as curr_app
from app.services.get_cotation_info_service import get_cotation_info
from app.services.register_cotation import register_cotation
from app.utils import fetch


def get_conversion_service():
    from_currency = curr_app.from_currency
    to_currency = curr_app.to_currency
    _from = from_currency.code
    to = to_currency.code
    amount = curr_app.amount_param
    conversion = ...
    quote_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _from == to:
        msg = {"message": "Nothing to convert."}
        return msg

    elif curr_app.cotation:
        cot_rate = curr_app.cotation.rate
        conversion = (
            amount / cot_rate if curr_app.inverted_conversion else amount * cot_rate
        )
        quote_date = curr_app.cotation.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    elif from_currency.is_crypto:
        cot_rate, quote_date = get_cotation_info(from_currency, to_currency)
        conversion = amount * cot_rate

    elif to_currency.is_crypto:
        cot_rate, quote_date = get_cotation_info(from_currency, to_currency)
        conversion = amount / cot_rate

    else:
        conversion_data = fetch(_from, to)

        _from = (
            conversion_data["codein"]
            if curr_app.inverted_conversion
            else conversion_data["code"]
        )
        to = (
            conversion_data["code"]
            if curr_app.inverted_conversion
            else conversion_data["codein"]
        )
        quote_date = conversion_data["create_date"]

        rate = conversion_data.get("high", 1)

        rate = 1 / float(rate) if curr_app.inverted_conversion else rate

        conversion = amount * float(rate)

        register_cotation(rate, quote_date, from_currency, to_currency)

        payload = {"amount": curr_app.amount_param, **conversion_data}

    payload = {
        _from: round(amount, 4),
        to: round(conversion, 4),
        "quote_date": quote_date,
    }

    return payload
