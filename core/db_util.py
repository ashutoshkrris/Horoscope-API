import sqlite3
import threading
from datetime import datetime, timedelta

# Use in-memory database
DB_PATH = ':memory:'

# Thread-safe connection & lock
lock = threading.Lock()
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row


def init_db():
    with lock:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS daily_horoscope (
            sign TEXT,
            day TEXT,
            date TEXT,
            data TEXT,
            last_updated TIMESTAMP,
            PRIMARY KEY (sign, day)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS weekly_horoscope (
            sign TEXT,
            week TEXT,
            data TEXT,
            last_updated TIMESTAMP,
            PRIMARY KEY (sign)
        )
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS monthly_horoscope (
            sign TEXT,
            month TEXT,
            data TEXT,
            standout_days TEXT,
            challenging_days TEXT,
            last_updated TIMESTAMP,
            PRIMARY KEY (sign)
        )
        """)

        conn.commit()


# DAILY
def get_daily_horoscope(sign, day):
    with lock:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM daily_horoscope WHERE sign=? AND day=?
        """, (sign.lower(), day.lower()))
        row = cur.fetchone()

        if row:
            return {
                "date": row["date"].title(),
                "horoscope_data": row["data"]
            }
        return None


def save_daily_horoscope(sign, day, date, data):
    with lock:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO daily_horoscope (sign, day, date, data, last_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (sign.lower(), day.lower(), date, data, datetime.now()))
        conn.commit()


# WEEKLY
def get_weekly_horoscope(sign):
    with lock:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM weekly_horoscope WHERE sign=?
        """, (sign.lower(),))
        row = cur.fetchone()

        if row:
            current_week = get_current_week_range()
            if row["week"] == current_week.lower():
                return {
                    "week": row["week"].title(),
                    "horoscope_data": row["data"]
                }
        return None


def save_weekly_horoscope(sign, week, data):
    with lock:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO weekly_horoscope (sign, week, data, last_updated)
            VALUES (?, ?, ?, ?)
        """, (sign.lower(), week.lower(), data, datetime.now()))
        conn.commit()


# MONTHLY
def get_monthly_horoscope(sign):
    with lock:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM monthly_horoscope WHERE sign=?
        """, (sign.lower(),))
        row = cur.fetchone()

        if row:
            current_month = get_current_month()
            if row["month"] == current_month.lower():
                return {
                    "month": row["month"].title(),
                    "horoscope_data": row["data"],
                    "standout_days": row["standout_days"],
                    "challenging_days": row["challenging_days"]
                }
        return None


def save_monthly_horoscope(sign, month, data, standout_days, challenging_days):
    with lock:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO monthly_horoscope (sign, month, data, standout_days, challenging_days, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sign.lower(), month.lower(), data, standout_days, challenging_days, datetime.now()))
        conn.commit()


# UTILS
def get_current_week_range():
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return f"{start.strftime('%b')} {start.day}, {start.year} - {end.strftime('%b')} {end.day}, {end.year}".lower()


def get_current_month():
    today = datetime.now()
    return today.strftime("%B %Y").lower()


def purge_old_data():
    """Optional: cleanup data older than a threshold"""
    with lock:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM daily_horoscope WHERE last_updated < datetime('now', '-2 days')"
        )
        cur.execute(
            "DELETE FROM weekly_horoscope WHERE last_updated < datetime('now', '-8 days')"
        )
        cur.execute(
            "DELETE FROM monthly_horoscope WHERE last_updated < datetime('now', '-32 days')"
        )
        conn.commit()


# # Initialize the DB schema at import
# init_db()
