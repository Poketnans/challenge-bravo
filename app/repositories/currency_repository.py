from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Query, Session

from app.classes.app_with_db import current_app
from app.models import Currency


class CurrencyRepo:
    session: Session
    repo: Query[Currency]

    def __init__(self):
        self.session = current_app.db.session
        self.repo = self.session.query(Currency)

    def __enter__(self):
        return self

    def __exit__(self):
        self.session.commit()

    def get_by_id(self, id) -> Currency:
        return self.repo.get(id)

    def get_by(self, **queryDict) -> Currency:
        return self.repo.filter_by(**queryDict).first()

    def create(self, data):
        instance = Currency(**data)
        self.session.add(instance)
        return instance

    def update(self, data, **criteria):
        instance = self.repo.filter_by(**criteria)
        instance.update({**data, "updated_at": datetime.now()})
        return instance
