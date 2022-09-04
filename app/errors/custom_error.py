class CustomError(Exception):
    """
    Basis class used for typing concerns.
    """

    description: dict
    code: int
