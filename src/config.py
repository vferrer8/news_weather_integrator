import os

# Get environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

NEWS_BASE_URL = "https://newsapi.org/v2/everything"
WEATHER_BASE_URL = "https://history.openweathermap.org/data/2.5/history/city"

DEFAULT_UNITS= "metric" # "standard", "metric", "imperial"

MAX_NUM_CALLS = os.getenv('MAX_NUM_CALLS', 10)
CALL_PERIOD = os.getenv('CALL_PERIOD', 60) # in seconds