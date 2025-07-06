import logging
import re

import requests
from bs4 import BeautifulSoup

from core.zodiac_signs import ZodiacSign

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(levelname)s : %(message)s"
)

PARSER = "html.parser"
STANDOUT_DAYS_PATTERN = r"Standout (?:days|dates): ([\d, ]+)"
CHALLENGING_DAYS_PATTERN = r"Challenging (?:days|dates): ([\d, ]+)"


def get_horoscope_by_day(zodiac_sign: str, day: str):
    logging.info(
        f"get_horoscope_by_day::Started getting horoscope by day for {zodiac_sign=}, {day=}"
    )
    sign_value = ZodiacSign.get_sign_value(zodiac_sign)
    logging.info(f"get_horoscope_by_day::{sign_value=}")
    if "-" not in day:
        res = requests.get(
            f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day.lower()}.aspx?sign={sign_value}"
        )
    else:
        day = day.replace("-", "")
        res = requests.get(
            f"https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign={sign_value}&laDate={day}"
        )
    soup = BeautifulSoup(res.content, PARSER)
    data = soup.find("div", attrs={"class": "main-horoscope"})
    logging.info(f"get_horoscope_by_day::Scraped data = {data.p.text}")
    date, horoscope_data = data.p.text.split(" - ", 1)
    logging.info(
        f"get_horoscope_by_day::Completed getting horoscope by day for {zodiac_sign=}, {day=}"
    )
    return date, horoscope_data


def get_horoscope_by_week(zodiac_sign: str):
    logging.info(
        f"get_horoscope_by_week::Started getting horoscope by day for {zodiac_sign=}"
    )
    sign_value = ZodiacSign.get_sign_value(zodiac_sign)
    logging.info(f"get_horoscope_by_week::{sign_value=}")
    res = requests.get(
        f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-weekly.aspx?sign={sign_value}"
    )
    soup = BeautifulSoup(res.content, PARSER)
    data = soup.find("div", attrs={"class": "main-horoscope"})
    logging.info(f"get_horoscope_by_week::Scraped data = {data.p.text}")
    start_day, end_day, *horoscope_data = data.p.text.split(" - ")
    week = f"{start_day} - {end_day}"
    logging.info(
        f"get_horoscope_by_week::Completed getting horoscope by day for {zodiac_sign=}"
    )
    return week, horoscope_data[0]


def get_horoscope_by_month(zodiac_sign: str):
    logging.info(
        f"get_horoscope_by_month::Started getting horoscope by day for {zodiac_sign=}"
    )
    sign_value = ZodiacSign.get_sign_value(zodiac_sign)
    logging.info(f"get_horoscope_by_week::{sign_value=}")
    res = requests.get(
        f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-monthly.aspx?sign={sign_value}"
    )
    soup = BeautifulSoup(res.content, PARSER)
    data = soup.find("div", attrs={"class": "main-horoscope"})
    month, *horoscope_data = data.p.text.split(" - ")
    logging.info(f"get_horoscope_by_month::Scraped data = {data.p.text}")
    (
        standout_days,
        challenging_days,
        horoscope_cleaned_data,
    ) = get_standing_challenging_days(horoscope_data[0])
    logging.info(
        f"get_horoscope_by_month::Completed getting horoscope by day for {zodiac_sign=}"
    )
    return month, horoscope_cleaned_data, standout_days, challenging_days


def get_standing_challenging_days(text):
    standout_match = re.search(STANDOUT_DAYS_PATTERN, text)
    challenging_match = re.search(CHALLENGING_DAYS_PATTERN, text)
    if standout_match:
        standout_days = standout_match.group(1)
    else:
        standout_days = ""

    if challenging_match:
        challenging_days = challenging_match.group(1)
    else:
        challenging_days = ""

    temp = re.sub(STANDOUT_DAYS_PATTERN, "", text)
    temp = re.sub(CHALLENGING_DAYS_PATTERN, "", temp)
    cleaned_up_data = temp.replace("Good luck this month", " Good luck this month")

    return standout_days, challenging_days, cleaned_up_data
