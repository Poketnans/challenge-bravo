from typing import TYPE_CHECKING, TypedDict

from app.classes import current_app

if TYPE_CHECKING:
    from app.models.cotations_model import Cotation


class FieldsToUpdate(TypedDict):
    rate: float
    quote_date: str


def update_cotation(cotation: "Cotation", data: FieldsToUpdate):
    """
    Updates cotation.
    """
    session = current_app.db.session
    cotation = current_app.cotation

    for field, value in data.items():
        setattr(cotation, field, value)

    session.add(cotation)
    session.commit()
