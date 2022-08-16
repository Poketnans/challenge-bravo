from __future__ import annotations

from typing import TYPE_CHECKING

from app.utils.fetch import fetch
from app.utils.get_crypto_rate import get_crypto_rate
from app.utils.get_quote_date import get_quote_date
from app.utils.get_rate import get_rate

from .check_cotation_is_updated import check_cotation_is_updated

if TYPE_CHECKING:
    from app.models import Currency


def get_cotation(from_currency: "Currency", to_currency: "Currency"):
    from app.repositories.cotation_repository import CotationRepo
    from app.services.create_or_update_service import create_or_update

    repo = CotationRepo()
    cotation = repo.get_by(code=f"{from_currency.code}{to_currency.code}")

    if not cotation or check_cotation_is_updated(cotation):
        cotation_data = fetch(from_currency.code, to_currency.code)
        cotation_rate = (
            get_crypto_rate(get_rate(cotation_data))
            if from_currency.is_crypto
            else float(get_rate(cotation_data))
        )
        cotation_quote_date = get_quote_date(cotation_data)

        cotation = create_or_update(
            from_currency, to_currency, cotation_rate, cotation_quote_date, cotation
        )

    return cotation
