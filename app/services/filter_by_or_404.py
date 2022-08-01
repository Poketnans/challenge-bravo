from typing import Type

from flask_sqlalchemy import Model
from sqlalchemy.orm import Query
from werkzeug.exceptions import NotFound


def filter_by_or_404(
    query: Query, criteria, description=None, exception: Type[NotFound] = NotFound
) -> Model:
    """
    Runs the method `Query.filter_by` using given criteria. Returns the filtered register.

    `query` - the query over wich will be runned the filtering criteria

    `descrition` - custom description to pass to the exception call

    `exception` - a custom subclass of `werkzeug.exceptions.NotFound` that will be used for raise exception

    Example::

        query = session.query(Model)

        currency = filter_by_or_404(query, {"code": "USD"}, exception=CurrencyNotFoundError)

    """
    register = query.filter_by(**criteria).first()
    if not register:
        raise exception(description) if description else exception

    return register
