from abc import ABC, abstractmethod
from typing import List

from telebot.models import UserPoll, BaseWeather


class WeatherAbstract(ABC):
    @abstractmethod
    def get_weather_by_city(self, city_name: str) -> BaseWeather:
        raise NotImplementedError()


class CurrencyConversionAbstract(ABC):
    @abstractmethod
    def convert_currency(self, amount: float, from_code: str, to_code: str) -> float:
        raise NotImplementedError()


class RandomAnimalAbstract(ABC):
    @abstractmethod
    async def get_random_animal_image_url(self) -> str:
        raise NotImplementedError()


class CreatePollsAbstract(ABC):
    @abstractmethod
    def create_user_poll(self, poll_id: str, question: str, options: List[str], owner_id: str) -> str:
        """
        Create {UserPoll} object and return str id of new poll
        :param poll_id:
        :param question:
        :param options:
        :param owner_id:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_poll_by_id(self, poll_id: str) -> UserPoll:
        raise NotImplementedError()


class Service:
    def __init__(
            self,
            weather_service: WeatherAbstract,
            currency_conversion_service: CurrencyConversionAbstract,
            random_animal_service: RandomAnimalAbstract,
            create_polls_service: CreatePollsAbstract,
    ):
        self.weather_service: WeatherAbstract = weather_service
        self.currency_conversion_service: CurrencyConversionAbstract = currency_conversion_service
        self.random_animal_service: RandomAnimalAbstract = random_animal_service
        self.create_polls_service: CreatePollsAbstract = create_polls_service
