from .polls_handlers import register_create_send_polls_handlers
from .currency_conversion_handlers import register_currency_conversion_handlers
from .animal_handlers import register_random_animal_handler
from .start_handlers import register_start_handlers
from .weather_handlers import register_weather_handlers

__all__ = [
    register_start_handlers,
    register_weather_handlers,
    register_create_send_polls_handlers,
    register_random_animal_handler,
    register_currency_conversion_handlers
]
