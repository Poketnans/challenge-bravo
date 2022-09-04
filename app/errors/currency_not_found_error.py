from werkzeug.exceptions import NotFound

from .custom_error import CustomError


class CurrencyNotFoundError(CustomError, NotFound):
    description = {
        "error": "Currency not found.",
    }
