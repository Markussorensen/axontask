import openmeteo_requests
import pandas as pd
import numpy as np
from openmeteo_requests.Client import OpenMeteoRequestsError


def get_weather_data(params, openmeteo, url="https://archive-api.open-meteo.com/v1/archive"):
    """
    Get weather data from the openmeteo api
    """
    if "temperature_unit" in params:
        params["temperature_unit"] = params["temperature_unit"].lower()
    try:
        response = openmeteo.weather_api(url, params=params)
    except Exception as e:
        response = [e]
    return response[0]

def get_weather_info_from_response(apiresponse, response_json):
    """
    Get weather info from the response by calling and saving all info in a string to parse to the model later.
    """
    # if an error occured while fetching the data from API the apiresponse is a string
    if isinstance(apiresponse, OpenMeteoRequestsError):
        return str(apiresponse)

    # Dictionary to store the output data
    output_data = {}

    # Extract hourly data
    if "hourly" in response_json:
        hourly_params = response_json["hourly"]
        if len(hourly_params) > 0:
            hourly = apiresponse.Hourly()
            hourly_data = {"date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )}
            output_data["hourly_timestamps"] = hourly_data["date"]
            for i, param in enumerate(hourly_params):
                output_data[f"hourly_{param}"] = hourly.Variables(i).ValuesAsNumpy()
                output_data[f"hourly_{param}_avg"] = np.nanmean(output_data[f"hourly_{param}"])
                output_data[f"hourly_{param}_max"] = np.nanmax(output_data[f"hourly_{param}"])
                output_data[f"hourly_{param}_min"] = np.nanmin(output_data[f"hourly_{param}"])

    # Extract daily data
    if "daily" in response_json:
        daily_params = response_json["daily"]
        if len(daily_params) > 0:
            daily = apiresponse.Daily()
            daily_data = {"date": pd.date_range(
                start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
                end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = daily.Interval()),
                inclusive = "left"
            )}
            output_data["daily_timestamps"] = daily_data
            for i, param in enumerate(daily_params):
                output_data[f"daily_{param}"] = daily.Variables(i).ValuesAsNumpy()
                output_data[f"daily_{param}_avg"] = np.nanmean(output_data[f"daily_{param}"])
                output_data[f"daily_{param}_max"] = np.nanmax(output_data[f"daily_{param}"])
                output_data[f"daily_{param}_min"] = np.nanmin(output_data[f"daily_{param}"])

    return output_data