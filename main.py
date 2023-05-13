from ratelimit import RateLimitException
from src.data_collector import collect_data
from fastapi import FastAPI, HTTPException, Query
from src.config import DEFAULT_UNITS, MAX_NUM_CALLS, CALL_PERIOD
from src.models import Article, ServerError
import uvicorn
import structlog

log = structlog.get_logger()

description = """
The **News and Weather Integrator API** collects and integrates data from the following data sources:

- https://newsapi.org
- https://openweathermap.org

This API allow users to gather historical articles that contain weather statistical data, this can provide a broad training dataset to be used for predicting future natural disasters based on weather forecast.
"""

app = FastAPI(title="News and Weather Integrator API", description=description)

topic_description = "Keywords or phrases to search for in the article title and body."
lat_description = "Latitude of the city to analyze in decimal degrees."
lon_description = "Longitude of the city to analyze in decimal degrees."
num_days_description = "Number of days of the analysis period to calculate statistical weather data."
units_description = "Units for the weather data. Possible values are: standard, metric, imperial."

@app.get("/articles", responses = {500: {"model": ServerError}})
def collect_articles(topic: str = Query(...,description=topic_description), lat_analysis: float=Query(...,description=lat_description), lon_analysis: float=Query(...,description=lon_description), num_days_analysis: int=Query(default=5,description=num_days_description), weather_units=Query(default=DEFAULT_UNITS,description=units_description)) -> list[Article]:
    try: 
        log.info("Collecting data from News API and Weather API ...")
        articles = collect_data(
            topic=topic,
            lat_analysis=lat_analysis,
            lon_analysis=lon_analysis,
            num_days_analysis=num_days_analysis,
            weather_units=weather_units
        )
        return articles
    except RateLimitException as ex:
        message = f"More than {MAX_NUM_CALLS} in {CALL_PERIOD} seconds. Please, try again later."
        log.exception(message, error=repr(ex))
        raise HTTPException(
                status_code=429,
                detail=f"API request rate limit exceeded: {repr(ex)}",
            )
    except Exception as ex:
        log.exception("Validation Error for the input parameters", error=repr(ex))
        raise HTTPException(
                status_code=500,
                detail=f"An internal server error has occured: {repr(ex)}",
            )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)