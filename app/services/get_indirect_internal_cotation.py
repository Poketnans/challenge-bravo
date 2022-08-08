from sqlalchemy.orm import Query

from app.classes.app_with_db import current_app as curr_app
from app.models import Cotation, Currency
from app.services.create_or_update_service import create_or_update
from app.utils.get_cotation import get_cotation


def get_indirect_internal_cotation(internal: Currency, external: Currency) -> Cotation:
    session = curr_app.db.session
    query: Query[Cotation] = session.query(Cotation)
    currency_query: Query[Currency] = session.query(Currency)

    usd_curr = currency_query.filter_by(code="USD").first()

    USD_to_internal_cotation = get_cotation(query, usd_curr, internal)
    USD_to_external_cotation = get_cotation(query, usd_curr, external)

    cot_rate = USD_to_internal_cotation.rate / USD_to_external_cotation.rate

    cotation = create_or_update(
        internal, external, cot_rate, USD_to_external_cotation.quote_date
    )

    return cotation
