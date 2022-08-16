from app.classes.app_with_db import current_app
from app.models import Currency
from app.repositories import CotationRepo, CurrencyRepo
from app.services.create_or_update_service import create_or_update
from app.utils import get_cotation


def get_crypto_to_crypto_cotation(crypto_1: Currency, crypto_2: Currency):
    """
    Deals with crypto to crypto case across `crypto_to_USD` cotation.

    Aplies `rate = crypto_1_to_USD_cotation.rate / crypto_2_to_USD_cotation` logic
    """
    currency_repo = CurrencyRepo()

    usd_curr = currency_repo.get_by(code="USD")

    crypto_1_to_USD_cotation = get_cotation(crypto_1, usd_curr)
    crypto_2_to_USD_cotation = get_cotation(crypto_2, usd_curr)

    rate = crypto_1_to_USD_cotation.rate / crypto_2_to_USD_cotation.rate

    cotation = create_or_update(
        crypto_1,
        crypto_2,
        rate,
        crypto_1_to_USD_cotation.quote_date,
        current_app.cotation,
    )

    return cotation
