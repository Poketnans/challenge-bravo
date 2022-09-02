from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.cotations_model import Cotation


def check_cotation_is_updated(cotation: "Cotation") -> bool:
    """
    Checks if the cotation is updated.
    """
    now = datetime.now()
    last_update = cotation.updated_at
    elapsed_time = (now - last_update).total_seconds()

    update_sec_period = 60

    is_updated = elapsed_time < update_sec_period

    return is_updated
