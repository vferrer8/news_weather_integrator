from src.data_collector import collect_data

extreme_temp_spain_data = collect_data(
    topic="extreme temperature Spain",
    lat_analysis=40.4637,
    lon_analysis=-3.7492,
    num_days_analysis=5,
    weather_units="metric"
)

print(extreme_temp_spain_data)