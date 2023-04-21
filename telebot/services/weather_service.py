from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError, UnauthorizedError
from pyowm.config import DEFAULT_CONFIG
from pyowm.weatherapi25.weather_manager import WeatherManager

from telebot.models import BaseWeather
from telebot.services.services import WeatherAbstract


class BaseWeatherServiceError(Exception):
    """
    Base weather service exception
    """
    pass


class CityNotFoundError(BaseWeatherServiceError):
    """
    Raise when search city was not found
    """
    pass


class WeatherApiUnauthorizedError(BaseWeatherServiceError):
    """
    Exception if api token is unavailable
    """
    pass


class WeatherService(WeatherAbstract):
    def __init__(self, weather_api_key):
        owm_config = DEFAULT_CONFIG
        owm_config['language'] = 'ru'

        self.owm = OWM(weather_api_key, config=owm_config)
        self.weather_manager: WeatherManager = self.owm.weather_manager()

    def get_weather_by_city(self, city_name: str) -> BaseWeather:
        try:
            observation = self.weather_manager.weather_at_place(city_name)
            search_weather = observation.weather
            return search_weather
        except NotFoundError as _exc:
            raise CityNotFoundError("City was not found")
        except UnauthorizedError as _exc:
            raise WeatherApiUnauthorizedError("Web token is not available")
