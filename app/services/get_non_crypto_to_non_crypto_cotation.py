from app.models import Currency
from app.repositories import CotationRepo
from app.utils import get_cotation


def get_non_crypto_to_non_crypto_cotation(
    from_currency: Currency, to_currency: Currency
):
    """
    Deals with non crypto currency to non crypto currency external cotation
    """
    cotation = get_cotation(from_currency, to_currency)
    return cotation
