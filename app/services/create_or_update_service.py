from datetime import datetime
from typing import TYPE_CHECKING, Union

from app.repositories.cotation_repository import (
    CotationFields,
    CotationRepo,
    PartialCotationFields,
)
from app.utils import check_cotation_is_updated

if TYPE_CHECKING:
    from app.models import Cotation, Currency


def create_or_update(
    from_currency: "Currency",
    to_currency: "Currency",
    rate: float,
    quote_date: datetime,
    cotation: Union["Cotation", None] = None,
):
    """
    Inserts or updates cotations depending on its ipdate state.
    """

    with CotationRepo() as repo:
        if not cotation:
            payload: CotationFields = {
                "from_currency": from_currency,
                "to_currency": to_currency,
                "quote_date": quote_date,
                "rate": rate,
            }
            cotation = repo.create(payload)

        elif not check_cotation_is_updated(cotation):
            data: PartialCotationFields = {
                "quote_date": quote_date,
                "rate": rate,
            }
            cotation = repo.update(cotation.id, data)

    return cotation
