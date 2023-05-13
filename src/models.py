from pydantic import BaseModel
from typing import Optional

class WeatherStats(BaseModel):
    feels_like_mean: float
    feels_like_std: float
    temp_mean: float
    temp_std: float
    temp_max_mean: float
    temp_max_std: float
    temp_min_mean: float
    temp_min_std: float

class Source(BaseModel):
    id: Optional[str]
    name: str

class Article(BaseModel):
    author: str
    content: str
    description: str
    publishedAt: str
    source: Source
    title: str
    url: str
    urlToImage: str
    weather_stats: WeatherStats
