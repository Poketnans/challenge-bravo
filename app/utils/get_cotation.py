from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Query

from app.utils.fetch import fetch
from app.utils.get_crypto_rate import get_crypto_rate
from app.utils.get_rate import get_rate

if TYPE_CHECKING:
    from app.models import Cotation, Currency


def get_cotation(
    query: Query["Cotation"], from_currency: "Currency", to_currency: "Currency"
):
    from app.services.create_or_update_service import create_or_update

    cotation = query.filter_by(code=f"{from_currency.code}{to_currency.code}").first()

    if not cotation:
        cotation_data = fetch(from_currency.code, to_currency.code)
        cotation_rate = (
            get_crypto_rate(get_rate(cotation_data))
            if from_currency.is_crypto
            else float(get_rate(cotation_data))
        )
        cotation_quote_date: str = cotation_data["create_date"]

        cotation = create_or_update(
            from_currency, to_currency, cotation_rate, cotation_quote_date
        )

    return cotation
