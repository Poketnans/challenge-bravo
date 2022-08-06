from alembic import op

from app.classes.app_with_db import current_app
from app.models import Currency
from app.utils import get_initial_currencies


def pupulate_is_external_currencies_column():
    """
    Populates the column `is_external` on currencies table. That solves the\n
    `Null` problem due to the populating occurs on the first migration on wich\n
    that column were not created yet.
    """
    queries = """
    UPDATE currencies c
    SET is_external = (
        CASE
            {}
        END
    )
    """

    when_then_args = [
        f"WHEN c.code = '{data['code']}' THEN {data['is_external']}"
        for data in get_initial_currencies()
    ]
    op.execute(queries.format(" ".join(when_then_args)))
