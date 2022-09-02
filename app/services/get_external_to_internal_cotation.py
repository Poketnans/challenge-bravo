from typing import TYPE_CHECKING

from app.repositories import CotationRepo, CurrencyRepo
from app.utils import get_cotation

from .create_or_update_service import create_or_update

if TYPE_CHECKING:
    from app.models import Currency


def get_external_to_internal_cotation(
    from_currency: "Currency", to_currency: "Currency"
):
    FROM_TO = "FROM_TO"
    TO_FROM = "TO_FROM"

    external, internal, direction = (
        (from_currency, to_currency, FROM_TO)
        if from_currency.is_external
        else (to_currency, from_currency, TO_FROM)
    )

    currency_repo = CurrencyRepo()
    cotation_repo = CotationRepo()

    USD_currency = currency_repo.get_by(code="USD")

    external_to_USD_cotation = get_cotation(external, USD_currency)
    USD_to_internal_currency = cotation_repo.get_by(code=f"USD{internal.code}")

    rate = external_to_USD_cotation.rate * USD_to_internal_currency.rate

    code_selector = {
        FROM_TO: f"{external.code}{internal.code}",
        TO_FROM: f"{internal.code}{external.code}",
    }

    cotaton_code = code_selector[direction]
    cotation = cotation_repo.get_by(code=cotaton_code)

    cotation = create_or_update(
        external, internal, rate, external_to_USD_cotation.quote_date, cotation
    )

    return cotation
