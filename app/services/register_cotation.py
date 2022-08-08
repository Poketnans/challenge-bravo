from datetime import datetime
from typing import TYPE_CHECKING, TypedDict

from app.classes import current_app
from app.models.cotations_model import Cotation

if TYPE_CHECKING:
    from app.models import Currency


class CotationFields(TypedDict):
    rate: float
    quote_date: datetime
    from_currency: "Currency"
    to_currency: "Currency"


def register_cotation(data: CotationFields):
    session = current_app.db.session

    cotation = Cotation(
        code=f"{data['from_currency'].code}{data['to_currency'].code}",
        rate=data["rate"],
        quote_date=data["quote_date"],
        from_currency=data["from_currency"],
        to_currency=data["to_currency"],
    )

    session.add(cotation)
    session.commit()

    return cotation
