import requests
from shapely.geometry import shape, Point

def get_weather_for_location(geojson_boundary):
    """
    Fetches 5-day weather forecast from Open-Meteo for the center of a farm.
    Returns a dictionary with weather data or None on failure.
    """
    if not geojson_boundary:
        return None

    try:
        # Calculate the centroid (center point) of the farm's GeoJSON boundary
        farm_shape = shape(geojson_boundary)
        centroid = farm_shape.centroid
        latitude = centroid.y
        longitude = centroid.x

        # Construct the Open-Meteo API URL
        api_url = (f"https://api.open-meteo.com/v1/forecast?"
                   f"latitude={latitude}&longitude={longitude}&"
                   f"daily=weathercode,temperature_2m_max,temperature_2m_min&"
                   f"timezone=auto&forecast_days=5")
        
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
        
        data = response.json()

        # Structure the data nicely for the template
        forecast = []
        for i in range(len(data['daily']['time'])):
            day_data = {
                'date': data['daily']['time'][i],
                'max_temp': data['daily']['temperature_2m_max'][i],
                'min_temp': data['daily']['temperature_2m_min'][i],
                'weather_code': data['daily']['weathercode'][i]
            }
            forecast.append(day_data)
        
        return forecast

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None