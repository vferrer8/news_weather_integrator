from typing import Any
import requests
import pandas as pd
from src.config import WEATHER_BASE_URL, WEATHER_API_KEY, NEWS_BASE_URL, NEWS_API_KEY, DEFAULT_UNITS, MAX_NUM_CALLS, CALL_PERIOD
from src.models import Article, WeatherStats
from dateutil.parser import parse
from datetime import timedelta
from ratelimit import limits
import structlog
import numpy as np

log = structlog.get_logger()


@limits(calls=MAX_NUM_CALLS, period=CALL_PERIOD)
def get_news_data(api_key: str, q: str) -> dict:
    """Gets the data from NewsAPI

    Args:
        api_key (str): api key to access NewsAPI
        q (str): Keywords or phrases to search for in the article title and body

    Returns:
        dict: Response from the NewsAPI
    """
    news_params = {
        "apiKey": api_key,
        "q": q,
    }
    response = requests.get(NEWS_BASE_URL, params=news_params).json()
    log.info(f"Response from news api: {response}")
    return response

def extract_end_timestamp(article: dict) -> int:
    """Extract the end time for the analysis period

    Args:
        article (dict): Article containing "publishedAt" keyword.

    Returns:
        int: End time timestamp (in seconds) for the analysis period.
    """
    # we use the publishedAt field to calculate start_time and end_time
    published_at_iso_format = article["publishedAt"]
    # convert iso str format to datetime
    end_datetime = parse(published_at_iso_format) 
    end_timestamp = end_datetime.timestamp()
    return int(end_timestamp)


def extract_start_timestamp(end_time: float, num_days: int) -> int:
    """Extract the the start time for the analysis period

    Args:
        days (int): Number of days before published article used to calculate statistics on the weather data

    Returns:
        int: Start time timestamp (in seconds) for the analysis period.
    """
    start_timestamp = end_time - timedelta(days=num_days).total_seconds()
    return int(start_timestamp)

@limits(calls=MAX_NUM_CALLS, period=CALL_PERIOD)
def get_weather_data(api_key: str, lat: float, lon: float, start: int, end: int, units: str) -> dict:
    """Get weather data for the selected data analysis period

     Args:
        appid (str): api key to access WeatherAPI
        lat (float): Latitude of the city to analyze in decimal degrees.
        lon (float): Longitude of the city to analyze in decimal degrees.
        start (int): Start date for the analysis period.
        end (int): End date for the analysis period.
        units (str): Units for the weather data. Possible values are: standard, metric, imperial.

     Returns:
        dict: Response from the WeatherAPI
     """

    weather_params = {
        "appid": api_key,
        "lat": lat,
        "lon": lon,
        "start": start,
        "end": end,
        "units": units,
    }
    response = requests.get(WEATHER_BASE_URL, params=weather_params).json()
    log.info(f"Response from weather api: {response}")
    return response


def get_weather_data_stats(hourly_weather_data: list[dict[str, Any]]) -> pd.DataFrame:
    weather_df = pd.DataFrame(columns=["feels_like", "humidity", "pressure", "temp", "temp_max", "temp_min"])
    for hour_spec in hourly_weather_data:
        hour_df = pd.DataFrame([hour_spec["main"]])
        weather_df = pd.concat([weather_df, hour_df], ignore_index=True)
    weather_df_stats = weather_df.describe()
    return weather_df_stats.replace({np.nan: None})

def integrate_data(article: dict[str, Any], weather_stats_df: pd.DataFrame) -> Article:
    weather_stats = WeatherStats(
        feels_like_mean=weather_stats_df["feels_like"]["mean"],
        feels_like_std=weather_stats_df["feels_like"]["std"],
        temp_mean=weather_stats_df["temp"]["mean"],
        temp_std=weather_stats_df["temp"]["std"],
        temp_max=weather_stats_df["temp_max"]["max"],
        temp_min=weather_stats_df["temp_min"]["min"],
    )
    log.info(weather_stats)
    return Article(**article,weather_stats=weather_stats)


def collect_data(topic: str, lat_analysis: float, lon_analysis: float, num_days_analysis: int=5, weather_units=DEFAULT_UNITS):
    news_data = get_news_data(api_key=NEWS_API_KEY, q= topic)
    integrated_articles = []

    for news_article in news_data["articles"]:
        end_time_analysis = extract_end_timestamp(article=news_article)
        start_time_analysis = extract_start_timestamp(end_time=end_time_analysis, num_days=num_days_analysis)
        try:
            weather_data = get_weather_data(api_key=WEATHER_API_KEY, lat=lat_analysis, lon=lon_analysis, start=start_time_analysis, end=end_time_analysis, units=weather_units)
        except:
            log.info("No weather data for this analysis period.")
            continue
        weather_data_stats = get_weather_data_stats(hourly_weather_data=weather_data["list"])
        integrated_article = integrate_data(article=news_article, weather_stats_df=weather_data_stats)
        integrated_articles.append(integrated_article)

    return integrated_articles
