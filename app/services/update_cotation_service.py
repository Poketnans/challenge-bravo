from datetime import datetime

from app.classes import current_app
from app.models.cotations_model import Cotation


def update_cotation(
    rate: float,
    quote_date: str,
):
    session = current_app.db.session
    cotation = current_app.cotation

    cotation.rate = rate
    cotation.updated_at = datetime.strptime(quote_date, "%Y-%m-%d %H:%M:%S")

    session.add(cotation)
    session.commit()
