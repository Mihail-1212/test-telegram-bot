import logging
from http import HTTPStatus
from urllib.parse import urljoin

import requests
from requests.models import PreparedRequest, Response

from telebot.services.services import CurrencyConversionAbstract

logger = logging.getLogger()


class BaseCurrencyError(Exception):
    """
    Base currency conversion service error
    """
    pass


class CurrencyBadRequestError(BaseCurrencyError):
    pass


class CurrencyUnknownError(BaseCurrencyError):
    pass


class CurrencyUnauthorizedError(BaseCurrencyError):
    """
    Exception on error token
    """
    pass


class CurrencyConversionService(CurrencyConversionAbstract):
    base_url = "https://api.apilayer.com/exchangerates_data/"

    def __init__(self, convert_currency_api_key):
        self.api_key: str = convert_currency_api_key

    def _get_api_url(self):
        return self.base_url

    def _prepare_request(self, url: str, method: str, params: dict) -> str:
        """
        Make full url from args
        :param url:
        :param method:
        :param params:
        :return: full url as string
        """
        # Add method
        url = urljoin(url, method)

        # Add params
        req = PreparedRequest()
        req.prepare_url(url, params)

        return req.url

    def _generate_default_headers(self) -> dict:
        return {
            "apikey": self.api_key
        }

    def _generate_default_payload(self) -> dict:
        return {}

    def _send_convert_request(self, params: dict) -> Response:
        url: str = self._prepare_request(url=self._get_api_url(), method="convert", params=params)
        headers = self._generate_default_headers()
        payload = self._generate_default_payload()

        response = requests.request(method="GET", url=url, headers=headers, data=payload)

        return response

    def convert_currency(self, amount: float, from_code: str, to_code: str) -> float:
        params = {
            "to": to_code,
            "from": from_code,
            "amount": amount,
        }

        response: Response = self._send_convert_request(params)
        status_code = response.status_code

        if status_code == HTTPStatus.OK:
            data = response.json()
            result = data["result"]
            return float(result)
        elif status_code == HTTPStatus.BAD_REQUEST:
            raise CurrencyBadRequestError()
        elif status_code == HTTPStatus.UNAUTHORIZED:
            raise CurrencyUnauthorizedError()
        logger.error(f"Unknown response code {status_code}", extra={
            "server_response": response,
            "user_params": params,
        })
        raise CurrencyUnknownError()
