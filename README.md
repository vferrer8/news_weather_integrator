# Data Integration Case

## Data Sources
- **OpenWeatherMap API** (https://openweathermap.org/api)
API used: https://openweathermap.org/history#min

- **NewsAPI** (https://newsapi.org/)

## How the application interacts with the APIs
Both APIs have python client libraries:
- **News API**: https://newsapi.org/docs/client-libraries/python
- **Weather**: https://pyowm.readthedocs.io

However, the application is using `requests` library.


## Get started
1. Create a virtual environment for this project with:
```
python -m venv venv
```
2. Activate the virtual environment
- For windows users:
```
.\venv\Scripts\activate
```
- For Linux / mac users:
```
source venv/bin/activate
```
3. Install the required dependencies for this project from the `requirements.txt`

```
pip install -r requirements.txt
```

4. Set ENVIRONMENT_VARIABLES

    For Windows:

    Create a `env.bat` file and add the following api keys:
    ```
    set WEATHER_API_KEY=
    set NEWS_API_KEY=
    ```
    Run the file with `env.bat`

    For Linux:

    Create a `env.sh` file and add the following api keys:
    ```
    export WEATHER_API_KEY=
    export NEWS_API_KEY=
    ```
    Run the file with `source env.sh`