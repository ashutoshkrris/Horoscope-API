from enum import Enum


class ZodiacSign(Enum):
    Aries = 1
    Taurus = 2
    Gemini = 3
    Cancer = 4
    Leo = 5
    Virgo = 6
    Libra = 7
    Scorpio = 8
    Sagittarius = 9
    Capricorn = 10
    Aquarius = 11
    Pisces = 12

    @classmethod
    def get_sign_value(cls, sign_name):
        return cls[sign_name.capitalize()].value
    
    @classmethod
    def get_all_signs(cls):
        return ", ".join(sign.name for sign in ZodiacSign)
