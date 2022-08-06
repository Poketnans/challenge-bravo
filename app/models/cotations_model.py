from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.configs.database import db
from app.models.currencies_model import Currency


@dataclass
class Cotation(db.Model):

    id: str
    code: str
    rate: float
    quote_date: datetime
    created_at: datetime
    updated_at: datetime
    from_currency: Currency
    to_currency: Currency

    __tablename__ = "cotations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    code = Column(String(50), unique=True, nullable=False)
    rate = Column(Float, nullable=False)
    quote_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    from_currency_id = Column(String, ForeignKey("currencies.id"))
    to_currency_id = Column(String, ForeignKey("currencies.id"))

    from_currency = relationship(
        "Currency",
        uselist=False,
        foreign_keys=from_currency_id,
        lazy="select",
    )

    to_currency = relationship(
        "Currency",
        uselist=False,
        foreign_keys=to_currency_id,
        lazy="select",
    )
