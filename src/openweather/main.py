import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if API_KEY:
    OPENWEATHER_API_URL = (
        "https://api.openweathermap.org/data/4.0/onecall/timeline/1day?lat=51.5&lon=-0.1&appid="
        + API_KEY
    )


def get_weather():
    print(OPENWEATHER_API_URL)


def main():
    print(get_weather())
