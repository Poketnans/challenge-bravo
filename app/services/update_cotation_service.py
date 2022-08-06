from datetime import datetime
from typing import TYPE_CHECKING, TypedDict, Union

from app.classes import current_app

if TYPE_CHECKING:
    from app.models.cotations_model import Cotation


class FieldsToUpdate(TypedDict, total=False):
    rate: float
    quote_date: Union[str, datetime]


def update_cotation(cotation: "Cotation", data: FieldsToUpdate):
    """
    Updates a cotation.
    """
    session = current_app.db.session

    for field, value in data.items():
        setattr(cotation, field, value)

    cotation.updated_at = datetime.now()

    session.add(cotation)
    session.commit()
