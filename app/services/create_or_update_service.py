from datetime import datetime
from typing import TYPE_CHECKING, Union

from app.services.register_cotation import register_cotation
from app.services.update_cotation_service import update_cotation
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
    if not cotation:
        new_cotation = register_cotation(
            {
                "rate": rate,
                "quote_date": quote_date,
                "from_currency": from_currency,
                "to_currency": to_currency,
            }
        )
        return new_cotation

    elif not check_cotation_is_updated(cotation):
        updated_cotation = update_cotation(
            cotation,
            {
                "rate": rate,
                "quote_date": quote_date,
            },
        )
        return updated_cotation

    return cotation
