import datetime

def userinput_to_data(user_query: str, extracted_queries) -> str:
    # Extract current date and time to make it easier for the model.
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    response_to_data = f"""
    We will access the Meteo Weather API to extract weather data. The options of parameters are given here, and your response needs to only be a JSON schema with parameters you want to answer the question:

    {{
        "latitude": , # float
        "longitude": , # float
        "start_date": , # String (yyyy-mm-dd)
        "end_date": , # String (yyyy-mm-dd)
        "hourly": , # String array	No		A list of weather variables which should be returned. Values can be comma separated, choices=[temperature_2m, relative_humidity_2m, dew_point_2m, apparent_temperature, pressure_msl, surface_pressure, precipitation, rain, snowfall, cloud_cover, cloud_cover_low, cloud_cover_mid, cloud_cover_high, shortwave_radiation, direct_radiation, direct_normal_irradiance, diffuse_radiation, global_tilted_irradiance, sunshine_duration, wind_speed_10m, wind_speed_100m, wind_direction_10m, wind_direction_100m, wind_gusts_10m, et0_fao_evapotranspiration, weather_code, snow_depth, vapour_pressure_deficit, soil_temperature_0_to_7cm, soil_temperature_7_to_28cm, soil_temperature_28_to_100cm, soil_temperature_100_to_255cm, soil_moisture_0_to_7cm, soil_moisture_7_to_28cm, soil_moisture_28_to_100cm, soil_moisture_100_to_255cm.] or multiple &hourly= parameter in the URL can be used.
        "daily": , # String array	No		A list of weather variables which should be returned. Values can be comma separated, choices=[weather_code, temperature_2m_max, temperature_2m_min, apparent_temperature_max, apparent_temperature_min, precipitation_sum, rain_sum, snowfall_sum, precipitation_hours, sunrise, sunset, sunshine_duration, daylight_duration, wind_speed_10m_max, wind_gusts_10m_max, wind_direction_10m_dominant, shortwave_radiation_sum, et0_fao_evapotranspiration.].
        "temperature_unit": , # String	No		Unit of temperature. Default is Celsius Possible values are Celsius, Fahrenheit.
        "wind_speed_unit": , # String	No		Unit of wind speed. Default is kmh. Possible values are ms, kmh, mph, kn.
        "precipitation_unit": , # String	No		Unit of precipitation. Default is mm. Possible values are mm, inch.
        "call_selection": , # String	No		Set a preference how grid-cells are selected. The default land.
    }}

    If needed to make the right queries current date is {current_date}.
    
    The question from the user is:

    {user_query}

    You are allowed to make multiple queries. If so your response should be a list of JSON schemas with the parameters you want to extract. E.g.:

    [
    schema1,
    schema2,
    schema3
    ]
    """
    return response_to_data

def data_to_output(data, question):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    data_to_output = f"""
    The data extracted from the meteo weather api is as follows:

    {data}

    Make a response depending on the data extracted and the question asked below:

    {question}

    If you can use it to answer the question today is: {current_date}. Do not make the answer as if the user knows the data you extracted, just use it to answer the question.

    If the extracted data generated an error, Do not take that into account in the response, and try to respond to the question with you prior knowledge and the date provided above.

    """
    return data_to_output