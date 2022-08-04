def get_rate(conv_payload: dict) -> str:
    """
    Stracts the rate from conversion payload.
    """
    return conv_payload.get("high", 1)
