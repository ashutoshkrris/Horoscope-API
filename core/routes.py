import logging
from datetime import datetime

from flask import jsonify
from flask_restx import Resource, reqparse
from werkzeug.exceptions import BadRequest, NotFound

from core import api
from core.utils import (
    get_horoscope_by_day,
    get_horoscope_by_month,
    get_horoscope_by_week,
)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(levelname)s : %(message)s"
)

NOT_FOUND_MESSAGE = "No such zodiac sign exists"
BAD_REQUEST_MESSAGE = "Something went wrong, please check the URL and the arguments."


ns = api.namespace("/", description="Horoscope APIs")

parser = reqparse.RequestParser()
parser.add_argument("sign", type=str, required=True)

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
            f"DailyHoroscopeAPI::get::Arguments passed: {day=}, {zodiac_sign=}"
        )
        try:
            if "-" in day:
                day = datetime.strptime(day, "%Y-%m-%d")
            logging.info(
                f"DailyHoroscopeAPI::get::Calling get horoscope by day method with {day=}, {zodiac_sign=}"
            )
            date, horoscope_data = get_horoscope_by_day(zodiac_sign, day)
            data = {"date": date, "horoscope_data": horoscope_data}
            logging.info(
                f"DailyHoroscopeAPI::get::Completed getting daily horoscope with {data=}"
            )
            return jsonify(success=True, data=data, status=200)
        except KeyError as error:
            logging.error(f"DailyHoroscopeAPI::get", error)
            e = NotFound()
            e.data = {"status": e.code, "success": False, "message": NOT_FOUND_MESSAGE}
            raise e
        except AttributeError as error:
            logging.error(f"DailyHoroscopeAPI::get", error)
            e = BadRequest()
            e.data = {
                "status": e.code,
                "success": False,
                "message": "Invalid value passed in day argument.",
            }
            raise e
        except ValueError as error:
            logging.error(f"DailyHoroscopeAPI::get", error)
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
        logging.info("WeeklyHoroscopeAPI::get::Started getting weekly horoscope")
        args = parser.parse_args()
        zodiac_sign = args.get("sign")
        logging.info(f"WeeklyHoroscopeAPI::get::Arguments passed: {zodiac_sign=}")
        try:
            week, horoscope_data = get_horoscope_by_week(zodiac_sign)
            data = {"week": week, "horoscope_data": horoscope_data}
            logging.info(
                f"WeeklyHoroscopeAPI::get::Completed getting weekly horoscope with {data=}"
            )
            return jsonify(success=True, data=data, status=200)
        except KeyError as error:
            logging.error(f"WeeklyHoroscopeAPI::get", error)
            e = NotFound()
            e.data = {"status": e.code, "success": False, "message": NOT_FOUND_MESSAGE}
            raise e
        except AttributeError as error:
            logging.error(f"WeeklyHoroscopeAPI::get", error)
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
        logging.info("MonthlyHoroscopeAPI::get::Started getting weekly horoscope")
        args = parser.parse_args()
        zodiac_sign = args.get("sign")
        try:
            (
                month,
                horoscope_data,
                standout_days,
                challenging_days,
            ) = get_horoscope_by_month(zodiac_sign)
            data = {
                "month": month,
                "horoscope_data": horoscope_data,
                "standout_days": standout_days,
                "challenging_days": challenging_days,
            }
            logging.info(
                f"MonthlyHoroscopeAPI::get::Completed getting weekly horoscope with {data=}"
            )
            return jsonify(success=True, data=data, status=200)
        except KeyError as error:
            logging.error(f"MonthlyHoroscopeAPI::get", error)
            e = NotFound()
            e.data = {"status": e.code, "success": False, "message": NOT_FOUND_MESSAGE}
            raise e
        except AttributeError as error:
            logging.error(f"MonthlyHoroscopeAPI::get", error)
            e = BadRequest()
            e.data = {
                "status": e.code,
                "success": False,
                "message": BAD_REQUEST_MESSAGE,
            }
            raise e
