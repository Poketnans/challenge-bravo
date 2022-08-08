from sqlalchemy.orm import Query

from app.classes.app_with_db import current_app as curr_app
from app.models import Cotation, Currency
from app.services.create_or_update_service import create_or_update
from app.utils import get_cotation


def get_indirect_crypto_cotation(crypto: Currency, currency: Currency) -> Cotation:
    session = curr_app.db.session
    query: Query[Cotation] = session.query(Cotation)
    currency_query: Query[Currency] = session.query(Currency)

    usd_curr = currency_query.filter_by(code="USD").first()

    crypto_to_USD_cotation = get_cotation(query, crypto, usd_curr)
    USD_to_external = get_cotation(query, usd_curr, currency)

    cot_rate = crypto_to_USD_cotation.rate * float(USD_to_external.rate)

    cotation = create_or_update(crypto, currency, cot_rate, USD_to_external.quote_date)

    return cotation
