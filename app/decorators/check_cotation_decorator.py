from functools import wraps
from typing import Callable

from app.classes.app_with_db import current_app
from app.utils import check_cotation_is_updated


def check_cotation(controller: Callable) -> Callable:
    """
    Verifies if registered cotation is up to date in database and sets
    the `app.cotation_is_updated` to relative bollean.
    """

    @wraps(controller)
    def wrapper(*args, **kwargs) -> Callable:
        cotation = current_app.cotation

        if cotation:
            current_app.cotation_is_updated = check_cotation_is_updated(cotation)

        return controller(*args, **kwargs)

    return wrapper
