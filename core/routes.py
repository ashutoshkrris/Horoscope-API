import logging
from datetime import datetime

from flask import jsonify, make_response, request
from flask_restx import Resource, reqparse
import requests
from werkzeug.exceptions import BadRequest, NotFound

from core import api
from core.db_util import (
    get_daily_horoscope,
    save_daily_horoscope,
    get_weekly_horoscope,
    save_weekly_horoscope,
    get_monthly_horoscope,
    save_monthly_horoscope
)
from core.utils import (
    get_horoscope_by_day,
    get_horoscope_by_week,
    get_horoscope_by_month,
)
from core.zodiac_signs import ZodiacSign

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(levelname)s : %(message)s"
)

NOT_FOUND_MESSAGE = "No such zodiac sign exists"
BAD_REQUEST_MESSAGE = "Something went wrong, please check the URL and the arguments."

ns = api.namespace("/", description="Horoscope APIs")
health_ns = api.namespace("", description="Health Check API")

parser = reqparse.RequestParser()
parser.add_argument(
    "sign",
    type=str,
    required=True,
    help=f"Accepted values: {ZodiacSign.get_all_signs()}"
)

parser_copy = parser.copy()
parser_copy.add_argument(
    "day",
    type=str,
    required=False,
    default="TODAY",
    help='Accepted values: Date in format (YYYY-MM-DD) OR "TODAY" OR "TOMORROW" OR "YESTERDAY".',
)


@ns.route("/get-horoscope/daily")
class DailyHoroscopeAPI(Resource):
    """Shows daily horoscope of zodiac signs"""

    @ns.doc(parser=parser_copy)
    def get(self):
        logging.info("DailyHoroscopeAPI::get::Started getting daily horoscope")
        args = parser_copy.parse_args()
        day = args.get("day")
        zodiac_sign = args.get("sign")
        logging.info(
            f"DailyHoroscopeAPI::get::Arguments passed: {day=}, {zodiac_sign=}")

        try:
            if "-" in day:
                provided_date = datetime.strptime(day, "%Y-%m-%d")
                if provided_date > datetime.now():
                    e = BadRequest()
                    e.data = {
                        "status": e.code,
                        "success": False,
                        "message": "Future date is not supported!",
                    }
                    raise e

            # Check DB first
            cached = get_daily_horoscope(zodiac_sign, day)
            if cached:
                logging.info("Fetched details from cache")
                return jsonify(success=True, data=cached, status=200)

            # Scrape & save
            date, horoscope_data = get_horoscope_by_day(zodiac_sign, day)
            save_daily_horoscope(zodiac_sign, day, date, horoscope_data)

            data = {"date": date, "horoscope_data": horoscope_data}
            logging.info(f"DailyHoroscopeAPI::get::Completed with {data=}")
            return jsonify(success=True, data=data, status=200)

        except KeyError as error:
            logging.error(f"DailyHoroscopeAPI::get::{error}")
            e = NotFound()
            e.data = {"status": e.code, "success": False,
                      "message": NOT_FOUND_MESSAGE}
            raise e

        except AttributeError as error:
            logging.error(f"DailyHoroscopeAPI::get::{error}")
            e = BadRequest()
            e.data = {
                "status": e.code,
                "success": False,
                "message": "Invalid value passed in day argument.",
            }
            raise e

        except ValueError as error:
            logging.error(f"DailyHoroscopeAPI::get::{error}")
            e = BadRequest()
            e.data = {
                "status": e.code,
                "success": False,
                "message": "Please enter day in the correct format: YYYY-MM-DD",
            }
            raise e


@ns.route("/get-horoscope/weekly")
class WeeklyHoroscopeAPI(Resource):
    """Shows weekly horoscope of zodiac signs"""

    @ns.doc(parser=parser)
    def get(self):
        logging.info(
            "WeeklyHoroscopeAPI::get::Started getting weekly horoscope")
        args = parser.parse_args()
        zodiac_sign = args.get("sign")
        logging.info(
            f"WeeklyHoroscopeAPI::get::Arguments passed: {zodiac_sign=}")

        try:
            # Check DB
            cached = get_weekly_horoscope(zodiac_sign)
            if cached:
                logging.info("Fetched details from cache")
                return jsonify(success=True, data=cached, status=200)

            # Scrape & save
            week, horoscope_data = get_horoscope_by_week(zodiac_sign)
            save_weekly_horoscope(zodiac_sign, week, horoscope_data)

            data = {"week": week, "horoscope_data": horoscope_data}
            logging.info(f"WeeklyHoroscopeAPI::get::Completed with {data=}")
            return jsonify(success=True, data=data, status=200)

        except KeyError as error:
            logging.error(f"WeeklyHoroscopeAPI::get::{error}")
            e = NotFound()
            e.data = {"status": e.code, "success": False,
                      "message": NOT_FOUND_MESSAGE}
            raise e

        except AttributeError as error:
            logging.error(f"WeeklyHoroscopeAPI::get::{error}")
            e = BadRequest()
            e.data = {
                "status": e.code,
                "success": False,
                "message": BAD_REQUEST_MESSAGE,
            }
            raise e


@ns.route("/get-horoscope/monthly")
class MonthlyHoroscopeAPI(Resource):
    """Shows monthly horoscope of zodiac signs"""

    @ns.doc(parser=parser)
    def get(self):
        logging.info(
            "MonthlyHoroscopeAPI::get::Started getting monthly horoscope")
        args = parser.parse_args()
        zodiac_sign = args.get("sign")
        logging.info(
            f"MonthlyHoroscopeAPI::get::Arguments passed: {zodiac_sign=}")

        try:
            # Check DB
            cached = get_monthly_horoscope(zodiac_sign)
            logging.info("Fetched details from cache")
            if cached:
                return jsonify(success=True, data=cached, status=200)

            # Scrape & save
            month, horoscope_data, standout_days, challenging_days = get_horoscope_by_month(
                zodiac_sign)
            save_monthly_horoscope(
                zodiac_sign, month, horoscope_data, standout_days, challenging_days)

            data = {
                "month": month,
                "horoscope_data": horoscope_data,
                "standout_days": standout_days,
                "challenging_days": challenging_days,
            }
            logging.info(f"MonthlyHoroscopeAPI::get::Completed with {data=}")
            return jsonify(success=True, data=data, status=200)

        except KeyError as error:
            logging.error(f"MonthlyHoroscopeAPI::get::{error}")
            e = NotFound()
            e.data = {"status": e.code, "success": False,
                      "message": NOT_FOUND_MESSAGE}
            raise e

        except AttributeError as error:
            logging.error(f"MonthlyHoroscopeAPI::get::{error}")
            e = BadRequest()
            e.data = {
                "status": e.code,
                "success": False,
                "message": BAD_REQUEST_MESSAGE,
            }
            raise e


@health_ns.route("/healthcheck")
class HealthCheckAPI(Resource):
    """Performs a health check on daily, weekly, and monthly horoscope endpoints"""

    def get(self):
        base_url = request.host_url.rstrip('/') + api.prefix
        endpoints = [
            "/get-horoscope/daily?sign=aries&day=today",
            "/get-horoscope/weekly?sign=aries",
            "/get-horoscope/monthly?sign=aries",
        ]

        results = {}
        overall_status = "healthy"

        for endpoint in endpoints:
            try:
                full_url = f"{base_url}{endpoint}"
                logging.debug(f"HealthCheckAPI::get::Checking {full_url}")
                response = requests.get(full_url)

                if response.status_code == 200:
                    results[endpoint] = "healthy"
                else:
                    results[endpoint] = f"unhealthy (status code: {response.status_code})"
                    overall_status = "unhealthy"
            except requests.exceptions.RequestException as e:
                results[endpoint] = f"unhealthy (exception: {str(e)})"
                overall_status = "unhealthy"

        data = {
            "status": overall_status,
            "details": results
        }
        status_code = 200 if overall_status == "healthy" else 503
        return make_response(jsonify(success=(overall_status == "healthy"), data=data, status=status_code), status_code)
