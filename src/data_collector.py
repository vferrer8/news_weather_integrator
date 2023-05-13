from typing import Any, Literal
import requests
from pprint import pprint
import pandas as pd
from src.config import WEATHER_BASE_URL, WEATHER_API_KEY, NEWS_BASE_URL, NEWS_API_KEY, DEFAULT_UNITS
from src.models import Article, WeatherStats
from dateutil.parser import parse
from datetime import timedelta
from pprint import pprint


# remove this after testing
from .get_data_mess import news_response
from .get_data_mess import weather_response

def get_news_data(api_key: str, q: str) -> dict:
    return news_response
    news_params = {
        "apiKey": api_key,
        "q": q,
    }
    response = requests.get(NEWS_BASE_URL, params=news_params).json()
    return response

def extract_end_timestamp(article: dict) -> float:
    """Extract the end time for the analysis period

    Args:
        article (dict): Article containing "publishedAt" keyword.

    Returns:
        float: End time timestamp (in seconds) for the analysis period.
    """
    published_at_iso_format = article["publishedAt"]
    # convert iso str format to datetime
    end_datetime = parse(published_at_iso_format) 
    return end_datetime.timestamp()


def extract_start_timestamp(end_time: float, num_days: int) -> float:
    return end_time - timedelta(days=num_days).total_seconds()


def get_weather_data(api_key: str, lat: float, lon: float, start: int, end: int, units: str) -> dict:
    return weather_response
    weather_params = {
        "appid": api_key,
        "lat": lat,
        "lon": lon,
        "start": start,
        "end": end,
        "units": units,
    }
    response = requests.get(WEATHER_BASE_URL, params=weather_params).json()
    return response


def get_weather_data_stats(hourly_weather_data: list[dict[str, Any]]) -> pd.DataFrame:
    weather_df = pd.DataFrame(columns=["feels_like", "humidity", "pressure", "temp", "temp_max", "temp_min"])
    for hour_spec in hourly_weather_data:
        hour_df = pd.DataFrame([hour_spec["main"]]) # contains only one row
        weather_df = pd.concat([weather_df, hour_df], ignore_index=True)
    return weather_df.describe()

def integrate_data(article: dict[str, Any], weather_stats_df: pd.DataFrame) -> Article:
    weather_stats = WeatherStats(
        feels_like_mean=weather_stats_df["feels_like"]["mean"],
        feels_like_std=weather_stats_df["feels_like"]["std"],
        temp_mean=weather_stats_df["temp"]["mean"],
        temp_std=weather_stats_df["temp"]["std"],
        temp_max_mean=weather_stats_df["temp_max"]["mean"],
        temp_max_std=weather_stats_df["temp_max"]["std"],
        temp_min_mean=weather_stats_df["temp_min"]["mean"],
        temp_min_std=weather_stats_df["temp_min"]["std"],
    )
    return Article(**article,weather_stats=weather_stats)


def collect_data(topic: str, lat_analysis: float, lon_analysis: float, num_days_analysis: int=5, weather_units=DEFAULT_UNITS):
    news_data = get_news_data(api_key=NEWS_API_KEY, q= topic)
    integrated_articles = []

    for news_article in news_data["articles"]:
        end_time_analysis = extract_end_timestamp(article=news_article)
        start_time_analysis = extract_start_timestamp(end_time=end_time_analysis, num_days=num_days_analysis)
        weather_data = get_weather_data(api_key=WEATHER_API_KEY, lat=lat_analysis, lon=lon_analysis, start=start_time_analysis, end=end_time_analysis, units=weather_units)
      
        weather_data_stats = get_weather_data_stats(hourly_weather_data=weather_data["list"])
        integrated_article = integrate_data(article=news_article, weather_stats_df=weather_data_stats)
        integrated_articles.append(integrated_article)

    return integrated_articles
