from datetime import datetime, timedelta
import calendar

def seconds_until_end_of_day():
    """Calculates the number of seconds until the end of the current day (midnight)."""
    now = datetime.now()
    end_of_day = datetime.combine(now + timedelta(days=1), datetime.min.time())
    return int((end_of_day - now).total_seconds())

def seconds_until_end_of_week():
    """Calculates the number of seconds until the end of the current week (Sunday)."""
    now = datetime.now()
    days_until_sunday = 6 - now.weekday()  # Sunday is the 6th day of the week
    end_of_week = datetime.combine(now + timedelta(days=days_until_sunday + 1), datetime.min.time())
    return int((end_of_week - now).total_seconds())

def seconds_until_end_of_month():
    """Calculates the number of seconds until the end of the current month."""
    now = datetime.now()
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]  # Last day of current month
    end_of_month = datetime(now.year, now.month, last_day_of_month, 23, 59, 59)
    return int((end_of_month - now).total_seconds())
