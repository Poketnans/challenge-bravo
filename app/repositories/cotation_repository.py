from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, TypedDict

from sqlalchemy.orm import Query, Session
from typing_extensions import NotRequired

from app.classes.app_with_db import current_app
from app.models import Cotation

if TYPE_CHECKING:
    from app.models import Currency


class CotationFields(TypedDict):
    rate: float
    quote_date: datetime
    from_currency: "Currency"
    to_currency: "Currency"


class PartialCotationFields(TypedDict):
    rate: NotRequired[float]
    quote_date: NotRequired[datetime]


class CotationRepo:
    _session: Session
    _query: Query[Cotation]

    def __init__(self):
        self._session = current_app.db.session
        self._query = self._session.query(Cotation)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._session.commit()

    def get_by_id(self, id) -> Cotation:
        return self._query.get(id)

    def get_by(self, **queryDict) -> Cotation:
        return self._query.filter_by(**queryDict).first()

    def get_query(self):
        return self._query

    def create(self, data: CotationFields):
        code = f'{data["from_currency"].code}{data["to_currency"].code}'.upper()
        instance = Cotation(**data, code=code)
        self._session.add(instance)
        return instance

    def update(self, data: PartialCotationFields, **criteria) -> Cotation:
        instance = self._query.filter_by(**criteria).first()
        for key, value in data.items():
            setattr(instance, key, value)

        instance.updated_at = datetime.now()

        self._session.add(instance)
        return instance
