from werkzeug.exceptions import BadRequest

from .custom_error import CustomError


class InvalidValueTypesError(CustomError, BadRequest):
    def __init__(self, error_msg: str, extra_fields: dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.description = {"error": error_msg, **extra_fields}
