# Python 3 Aiogram Telebot

This is test telegram chatbot.

He has next commands:
```commandline
/start - Start conversation
/weather - Get weather from input place
/currencyconversion - Convert currency
/randomanimal - Get random picture of animal
/createsendpolls - Create polls and send to chat
```

Use:
- Python (v 3.8.1)
- pip (v 19.2.3)
- Aiogram (v 2.25)
- pyowm (library for openweather api)
- animality (library for random animal api)


Use apis:
- telegram api
- OpenWeatherMap api (throw pyowm) (https://openweathermap.org/api)
- animality api (throw python animality) (https://animality.xyz/)
- exchangerates api (https://exchangeratesapi.io/)

### Quick start

Install pip libs:

```commandline
pip install -r requirements.txt
```


Create .env file with api tokens inside (see .env.example).

Available .env vars:
- POLLING_SKIP_UPDATES (opt) - bool variable to skip all bot updates before start polling
- TELEBOT_API_TOKEN (req) - api token for telegram bot
- WEATHER_API_KEY (req) - api token for OpenWeatherApi (https://openweathermap.org/)
- CURRENCY_CONVERSION_API_TOKEN (req) - api token for ExchangeRatesApi (https://exchangeratesapi.io/)


Then start application:

```commandline
python main.py
```


### Application structure:

    .
    ├── telebot                     # Application src directory
    │   ├── commands                    # Directory with bot commands instances
    │   ├── handlers                    # Directory with bot handlers (commands, etc)
    │   ├── keyboards                   # Directory with keyboard instance creation funcs
    │   ├── models                      # Directory with used models
    │   ├── services                    # Directory with app services
    │   ├── middleware.py               # File with cusom middlewares
    │   └── sturtup_handlers.py         # File with start polling handlers inside
    ├── config.py                   # File contain constraints to use in app
    ├── main.py                     # Main file of application
    ├── .env                        # File within environment variables
    ├── requirements.txt            # Text requirements file within pip freeze modules
    └── README.md                   
