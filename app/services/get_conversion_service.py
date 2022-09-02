from datetime import datetime

from app.classes.app_with_db import current_app as curr_app
from app.models.cotations_model import Cotation
from app.services.get_crypto_to_crypto_cotation import get_crypto_to_crypto_cotation
from app.services.get_crypto_to_non_usd_external_cotation import (
    get_crypto_to_non_usd_external_cotation,
)
from app.services.get_external_to_internal_cotation import (
    get_external_to_internal_cotation,
)
from app.services.get_internal_to_internal_cotation import (
    get_internal_to_internal_cotation,
)
from app.services.get_non_crypto_to_non_crypto_cotation import (
    get_non_crypto_to_non_crypto_cotation,
)
from app.utils.get_cotation import get_cotation


def get_conversion_service():
    from_currency = curr_app.from_currency
    to_currency = curr_app.to_currency
    amount = curr_app.amount_param
    cotation: Cotation = curr_app.cotation
    conversion = ...

    if from_currency.code == to_currency.code:
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

    # Crypto to Crypto
    elif from_currency.is_crypto and to_currency.is_crypto:
        cotation = get_crypto_to_crypto_cotation(from_currency, to_currency)
        conversion = amount * cotation.rate

    # External to Internal
    elif from_currency.is_external and not to_currency.is_external:
        print("weww")
        cotation = get_external_to_internal_cotation(to_currency, from_currency)
        conversion = amount * cotation.rate

    # External to Internal Inverted
    elif to_currency.is_external and not from_currency.is_external:
        cotation = get_external_to_internal_cotation(to_currency, from_currency)
        conversion = amount / cotation.rate

    # Crypto to non usd external
    elif from_currency.is_crypto and not to_currency.backing_currency:
        cotation = get_crypto_to_non_usd_external_cotation(from_currency, to_currency)
        conversion = amount * cotation.rate

    # Crypto to non usd external inverted
    elif to_currency.is_crypto and not from_currency.backing_currency:
        cotation = get_crypto_to_non_usd_external_cotation(to_currency, from_currency)
        conversion = amount / cotation.rate

    # Crypto to USD
    elif from_currency.is_crypto and to_currency.backing_currency:
        cotation = get_cotation(from_currency, to_currency)
        conversion = amount * cotation.rate

    # Crypto to USD inverted
    elif to_currency.is_crypto and from_currency.backing_currency:
        cotation = get_cotation(to_currency, from_currency)
        conversion = amount / cotation.rate

    # Internal to Internal
    elif not from_currency.is_external and not to_currency.is_external:
        cotation = get_internal_to_internal_cotation(from_currency, to_currency)
        conversion = amount * cotation.rate

    else:
        cotation = get_non_crypto_to_non_crypto_cotation(from_currency, to_currency)
        conversion = amount * cotation.rate

    payload = {
        from_currency.code: round(amount, 4),
        to_currency.code: round(conversion, 4),
        "quote_date": cotation.quote_date.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return payload
