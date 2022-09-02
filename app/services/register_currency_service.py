from datetime import datetime

from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from app.classes.app_with_db import current_app
from app.errors import AlreadyRegisteredError
from app.models import Currency
from app.repositories import CotationRepo, CurrencyRepo
from app.repositories.cotation_repository import CotationFields


def register_currency_service():
    validated_data: dict = current_app.validated_data

    new_currency = Currency(
        code=validated_data["code"].upper(),
        label=validated_data["label"].title(),
        is_crypto=validated_data.get("is_crypto", False),
    )

    USD_currency = CurrencyRepo().get_by(code="USD")

    from_currency = USD_currency
    to_currency = new_currency

    conversion = validated_data["conversion"]
    USD_value: float = conversion["USD"]
    local_value: float = conversion["local"]

    rate = local_value / USD_value

    payload: CotationFields = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "quote_date": datetime.now(),
        "rate": round(rate, 4),
    }

    try:
        with CotationRepo() as cotation_repo:
            cotation_repo.create(payload)

        return new_currency
    except IntegrityError as err:
        is_unique_violation = isinstance(err.orig, UniqueViolation)

        check_field_error = lambda field: f"Key ({field})" in f"{err.orig}"

        error_in_code = check_field_error("code")
        error_in_label = check_field_error("label")

        if is_unique_violation and error_in_code:
            raise AlreadyRegisteredError("code")
        elif is_unique_violation and error_in_label:
            raise AlreadyRegisteredError("label")

        raise err
