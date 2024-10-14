from flask import Flask
from decouple import config
from flask_caching import Cache
from flask_restx import Api

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))
api = Api(
    app,
    version="2.0.3",
    title="Horoscope API",
    description="The Horoscope API offers a versatile solution for accessing daily, weekly, and monthly horoscope predictions tailored to each zodiac sign. With intuitive endpoints and a straightforward interface, developers can seamlessly integrate astrological insights into their applications. Whether providing users with daily guidance, weekly trends, or monthly forecasts, this API delivers accurate and personalized horoscope data in JSON format. Built on reliable infrastructure, the API ensures scalability and reliability, enabling it to handle varying levels of demand with minimal downtime. With customizable parameters, developers can fine-tune requests to meet specific requirements, enhancing user experiences with tailored astrological content. Comprehensive documentation accompanies the API, providing developers with all the information needed to integrate horoscope data seamlessly. Start leveraging the Horoscope API today to empower users with personalized astrological insights that resonate with their individual zodiac signs and life experiences.",
    license="MIT",
    contact="Ashutosh Krishna",
    contact_url="https://ashutoshkrris.in",
    contact_email="ashutoshbritish@gmail.com",
    doc="/",
    prefix="/api/v1",
)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

from core import routes
