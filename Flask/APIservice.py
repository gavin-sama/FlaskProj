import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime
from dataclasses import dataclass

@dataclass
class weatherData:
    time: str
    temperature: float
    is_day: str
    wind_speed: float

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Get latitude and longitude by city or zip code
def get_lat_lon(name):
    response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1&language=en').json()
    data = response.get('results', [])[0]
    lat, lon = data.get('latitude'), data.get('longitude')
    return lat, lon

# Get Weather
def get_current_weather(lat, lon):
    # Define the URL and parameters
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "is_day", "wind_speed_10m"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": "auto"
    }

    # Make the API call
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]  # Process the first response (assuming one location)

    # Extract current weather data
    current = response.Current()
    current_time = datetime.utcfromtimestamp(current.Time()).strftime('%Y-%m-%d %H:%M:%S')
    current_temperature_2m = round(current.Variables(0).Value(), 2)
    current_is_day = "Yes" if int(current.Variables(1).Value()) == 1 else "No"
    current_wind_speed_10m = round(current.Variables(2).Value(), 2)

    # Return a weatherData object
    return weatherData(
        time=current_time,
        temperature=current_temperature_2m,
        is_day=current_is_day,
        wind_speed=current_wind_speed_10m
    )

def main(name):
    lat, lon = get_lat_lon(name)
    weather_data = get_current_weather(lat, lon)
    return weather_data

if __name__ == "__main__":
    lat, lon = get_lat_lon("37421")
    print(get_current_weather(lat, lon))
