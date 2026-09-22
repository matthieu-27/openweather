from __future__ import annotations

import os

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

CITIES: dict[str, list[float]] = {
    "Saint Geours De Maremne": [43.683331, -1.233330],
    "Toulouse": [43.600000, 1.433333],
    "Mérignac (Bordeaux)": [44.836151, -0.580816],
}

OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather?"

API_KEY: str | None = os.getenv("OPENWEATHER_API_KEY")

if API_KEY:
    OW_API_KEY: str = str(API_KEY)


class Coord(BaseModel):
    lon: float
    lat: float


class WeatherItem(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


class Wind(BaseModel):
    speed: float
    deg: int


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    type: int
    id: int
    country: str
    sunrise: int
    sunset: int


class OpenWeatherResponse(BaseModel):
    coord: Coord
    weather: list[WeatherItem]
    base: str
    main: Main
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int


def get_weather(city: str) -> OpenWeatherResponse:
    url = str(
        OPENWEATHER_BASE_URL
        + "lat="
        + str(CITIES[city][0])
        + "&lon="
        + str(CITIES[city][1])
        + "&appid="
        + OW_API_KEY
    )
    response = requests.get(url)
    return OpenWeatherResponse.model_validate(response.json())


def fc(fahrenheit):
    return fahrenheit - 273.15


def main():
    for city in CITIES:
        report = get_weather(city)
        print(
            f"City: {city} Forecast: {report.weather[0].description} with a wind at {report.wind.speed * 3.6:.2f}km/h, it will feel like {fc(report.main.feels_like):.2f}°C With a minimum of {fc(report.main.temp_min):.2f}°C and a maximum of {fc(report.main.temp_max):.2f}°C"
        )
