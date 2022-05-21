from werkzeug import Response
from core import api
from flask import jsonify
from core.utils import get_horoscope_by_day, get_horoscope_by_week, get_horoscope_by_month
from flask_restx import Resource, reqparse
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime

NOT_FOUND_MESSAGE = 'No such zodiac sign exists'
BAD_REQUEST_MESSAGE = 'Something went wrong, please check the URL and the arguments.'


ns = api.namespace('/', description='Horoscope APIs')

ZODIAC_SIGNS = {
    "Aries": 1,
    "Taurus": 2,
    "Gemini": 3,
    "Cancer": 4,
    "Leo": 5,
    "Virgo": 6,
    "Libra": 7,
    "Scorpio": 8,
    "Sagittarius": 9,
    "Capricorn": 10,
    "Aquarius": 11,
    "Pisces": 12
}

parser = reqparse.RequestParser()
parser.add_argument('sign', type=str, required=True)

parser_copy = parser.copy()
parser_copy.add_argument('day', type=str, required=True,
                         help='Accepted values: Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY')


@ns.route('/get-horoscope/daily')
class DailyHoroscopeAPI(Resource):
    '''Shows daily horoscope of zodiac signs'''
    @ns.doc(parser=parser_copy)
    def get(self):
        args = parser_copy.parse_args()
        day = args.get('day')
        zodiac_sign = args.get('sign')
        try:
            zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
            if "-" in day:
                datetime.strptime(day, '%Y-%m-%d')
            date, horoscope_data = get_horoscope_by_day(zodiac_num, day)
            data = {'date': date, 'horoscope_data': horoscope_data}
            return jsonify(success=True, data=data, status=200)
        except KeyError:
            e = NotFound()
            e.data = {"status": e.code, "success": False,
                      "message": NOT_FOUND_MESSAGE}
            raise e
        except AttributeError:
            e = BadRequest()
            e.data = {"status": e.code, "success": False,
                      "message": "Invalid value passed in day argument."}
            raise e
        except ValueError:
            e = BadRequest()
            e.data = {"status": e.code, "success": False,
                      "message": "Please enter day in the correct format: YYYY-MM-DD"}
            raise e


@ns.route('/get-horoscope/weekly')
class WeeklyHoroscopeAPI(Resource):
    '''Shows weekly horoscope of zodiac signs'''
    @ns.doc(parser=parser)
    def get(self):
        args = parser.parse_args()
        zodiac_sign = args.get('sign')
        try:
            zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
            week, horoscope_data = get_horoscope_by_week(zodiac_num)
            data = {
                "week": week,
                "horoscope_data": horoscope_data
            }
            return jsonify(success=True, data=data, status=200)
        except KeyError:
            e = NotFound()
            e.data = {"status": e.code, "success": False,
                      "message": NOT_FOUND_MESSAGE}
            raise e
        except AttributeError:
            e = BadRequest()
            e.data = {"status": e.code, "success": False,
                      "message": BAD_REQUEST_MESSAGE}
            raise e


@ns.route('/get-horoscope/monthly')
class MonthlyHoroscopeAPI(Resource):
    '''Shows monthly horoscope of zodiac signs'''
    @ns.doc(parser=parser)
    def get(self):
        args = parser.parse_args()
        zodiac_sign = args.get('sign')
        try:
            zodiac_num = ZODIAC_SIGNS[zodiac_sign.capitalize()]
            month, horoscope_data = get_horoscope_by_month(zodiac_num)
            data = {
                "month": month,
                "horoscope_data": horoscope_data
            }
            return jsonify(success=True, data=data, status=200)
        except KeyError:
            e = NotFound()
            e.data = {"status": e.code, "success": False,
                      "message": NOT_FOUND_MESSAGE}
            raise e
        except AttributeError:
            e = BadRequest()
            e.data = {"status": e.code, "success": False,
                      "message": BAD_REQUEST_MESSAGE}
            raise e
