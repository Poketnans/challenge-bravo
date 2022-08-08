from datetime import datetime


def get_quote_date(data) -> datetime:
    """
    Retrieves `quote_date` from data
    """
    quote_date = data["create_date"]

    return datetime.strptime(quote_date, "%Y-%m-%d %H:%M:%S")
