def get_crypto_rate(rate: str) -> float:
    """
    Treats specific cryptocoin rate value. This is a treatment to specific\n
    used external API.
    """
    rate_parts = rate.split(".")
    thousand_part = rate_parts[0]
    center_part = rate_parts[1][:3]
    float_part = rate_parts[1][4:] if len(rate_parts[1]) > 3 else 0

    return float(f"{thousand_part}{center_part}.{float_part}")
