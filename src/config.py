import os

# Get environment variables
WEATHER_API_KEY = os.getenv('API_USER')
NEWS_API_KEY = os.getenv('API_PASSWORD')

NEWS_BASE_URL = "https://newsapi.org/v2/everything"
WEATHER_BASE_URL = "https://history.openweathermap.org/data/2.5/history/city"

DEFAULT_UNITS= "metric" # "standard", "metric", "imperial"