from pydantic import BaseModel
from typing import Optional

class WeatherStats(BaseModel):
    feels_like_mean: Optional[float]
    feels_like_std: Optional[float]
    temp_mean: Optional[float]
    temp_std: Optional[float]
    temp_max: Optional[float]
    temp_min: Optional[float]

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

class ServerError(BaseModel):
    detail: str