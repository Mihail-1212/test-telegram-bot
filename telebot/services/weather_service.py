from pyowm import OWM
from pyowm.config import DEFAULT_CONFIG
from pyowm.weatherapi25.weather import Weather
from pyowm.weatherapi25.weather_manager import WeatherManager

from telebot.services.services import WeatherAbstract


class WeatherService(WeatherAbstract):
    def __init__(self, weather_api_key):
        owm_config = DEFAULT_CONFIG
        owm_config['language'] = 'ru'

        self.owm = OWM(weather_api_key, config=owm_config)
        self.weather_manager: WeatherManager = self.owm.weather_manager()

    def get_weather_by_city(self, city_name: str) -> Weather:
        observation = self.weather_manager.weather_at_place(city_name)
        search_weather = observation.weather
        return search_weather
