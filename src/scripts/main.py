from omegaconf import OmegaConf
from transformers import pipeline
import google.generativeai as genai
import json
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

from src.lib.queries import userinput_to_data, data_to_output
from src.lib.weather import get_weather_data, get_weather_info_from_response

def main():
    # Load config
    config = OmegaConf.load("config/config.yaml")

    # Define openai client
    # client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    genai.configure(api_key="AIzaSyBihNbTOiCTWXxQAkh7T1GO-XJwc57SzaA")
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Define the transformer model pipeline
    # pipe = pipeline("text-generation", model="dfurman/CalmeRys-78B-Orpo-v0.1")
    method = "Google"

    # Meteo weather api
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # First user query
    user_query = input("Welcome to your weather guide, what can i help with? \n")
    # Run until user terminates
    while True:
        # Current extracted queries:
        extracted_data = []

        # Convert user query to input for the model
        model_input = userinput_to_data(user_query, extracted_data)

        # Call the transformer model
        if method == "Google":
            response = model.generate_content(model_input)
            response = response.text
            # Make a list of the json schemas
            response = response.strip('```json\n')
            response_json = json.loads(response)
        
        # Extract the data from the response for each of the schemas
        for schema in response_json:
            apiresponse = get_weather_data(schema, openmeteo)
            data = get_weather_info_from_response(apiresponse, schema)
            extracted_data.append(data)

        # Make response for user
        model_input = data_to_output(extracted_data, user_query)
        output = model.generate_content(model_input)
        output = output.text

        print(output)

        # Ask for new user query
        user_query = input("\nIs there anything else i can help with? (type No to terminate) \n")

        if user_query.lower() == "no":
            break

    print("Thank you for using the weather guide")

if __name__ == "__main__":
    main()
