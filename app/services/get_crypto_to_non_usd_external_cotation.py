from sqlalchemy.orm import Query

from app.classes.app_with_db import current_app as curr_app
from app.models import Cotation, Currency
from app.repositories import CurrencyRepo
from app.services.create_or_update_service import create_or_update
from app.utils import get_cotation


def get_crypto_to_non_usd_external_cotation(
    crypto: Currency, currency: Currency
) -> Cotation:
    usd_curr = CurrencyRepo().get_by_code("USD")

    crypto_to_USD_cotation = get_cotation(crypto, usd_curr)
    USD_to_external = get_cotation(usd_curr, currency)

    cot_rate = crypto_to_USD_cotation.rate * float(USD_to_external.rate)

    cotation = create_or_update(
        crypto, currency, cot_rate, USD_to_external.quote_date, curr_app.cotation
    )

    return cotation
