from app.models import Currency
from app.repositories import CotationRepo
from app.services.create_or_update_service import create_or_update


def get_internal_to_internal_cotation(internal_1: Currency, internal_2: Currency):
    """
    Deals with internal to internal case across `USD_to_internal` cotation.

    Aplies `rate = USD_to_int2_rate / USD_to_int1_rate` logic
    """
    repo = CotationRepo()

    USD_to_internal_1_cotation = repo.get_by(code=f"USD{internal_1.code}")
    USD_to_internal_2_cotation = repo.get_by(code=f"USD{internal_2.code}")

    rate = USD_to_internal_2_cotation.rate / USD_to_internal_1_cotation.rate

    cotation = create_or_update(
        internal_1, internal_2, rate, USD_to_internal_1_cotation.quote_date
    )

    return cotation
