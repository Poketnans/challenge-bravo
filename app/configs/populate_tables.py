from datetime import datetime
from uuid import uuid4

from alembic import op
from sqlalchemy import Table

from app.utils import get_initial_currencies


def populate_currencies_table(table: Table):
    rows = [
        {
            "id": str(uuid4()),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            **currency,
        }
        for currency in get_initial_currencies()
    ]

    op.bulk_insert(table, rows)
