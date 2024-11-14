from datetime import datetime


def validate_date_range(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if start > end:
            raise ValueError("Start date cannot be later than end date.")
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")


def parse_month(month_str):
    try:
        month = int(month_str)
        if 1 <= month <= 12:
            return month
        else:
            raise ValueError("Month must be between 1 and 12.")
    except ValueError:
        raise ValueError("Invalid month format.")
