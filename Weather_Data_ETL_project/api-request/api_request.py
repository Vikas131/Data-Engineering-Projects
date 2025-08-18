import requests, os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("WEATHERSTACK_API_KEY")
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"

def extract_data():
    print("Extracting weather data from Weatherstack API.")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print("API response received successfully.")
        return(response.json())

    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
        raise
