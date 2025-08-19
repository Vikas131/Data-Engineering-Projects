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

# extract_data()

def mock_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2025-08-12 03:03', 'localtime_epoch': 1754967780, 'utc_offset': '-4.0'}, 'current': {'observation_time': '07:03 AM', 'temperature': 23, 'weather_code': 113, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'], 'weather_descriptions': ['Clear '], 'astro': {'sunrise': '06:04 AM', 'sunset': '07:58 PM', 'moonrise': '09:42 PM', 'moonset': '09:42 AM', 'moon_phase': 'Waning Gibbous', 'moon_illumination': 91}, 'air_quality': {'co': '456.95', 'no2': '63.455', 'o3': '37', 'so2': '18.5', 'pm2_5': '38.295', 'pm10': '38.85', 'us-epa-index': '2', 'gb-defra-index': '2'}, 'wind_speed': 10, 'wind_degree': 240, 'wind_dir': 'WSW', 'pressure': 1021, 'precip': 0, 'humidity': 69, 'cloudcover': 0, 'feelslike': 25, 'uv_index': 0, 'visibility': 16, 'is_day': 'no'}}