from werkzeug.exceptions import Forbidden

from .custom_error import CustomError


class InitialCurrencyForbiddenError(CustomError, Forbidden):
    description = {
        "error": "This is a restrict currency. You can not delete it.",
    }
