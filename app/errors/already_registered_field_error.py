from werkzeug.exceptions import Conflict

from .custom_error import CustomError


class AlreadyRegisteredError(CustomError, Conflict):
    def __init__(self, field, description=None, response=None) -> None:
        super().__init__(description, response)
        self.description = {
            "error": "Unique violation error.",
            field: [f"This field is already registered."],
        }
