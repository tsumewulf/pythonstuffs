import json
import requests

base_url = "https://api.openweathermap.org/data/2.5/weather"
appid = "45e9330426a3f5665e493bdf23441954"

def get_weather(zip_or_city, units):
    """
    Get weather forecast data from openweathermap.org using a zip code or city name.
    Returns a dictionary containing the weather data.
    """
    try:
        if zip_or_city.isdigit():
            # If the user provided a 5-digit zip code, append the country code "US"
            zip_or_city += ",US"

        # Make a request to the openweathermap API using the zip code or city name and the specified units
        response = requests.get(f"{base_url}?q={zip_or_city}&units={units}&appid={appid}")

        # Check if the connection was successful
        if response.status_code == 200:
            # Parse the JSON data from the response into a dictionary
            weather_data = response.json()
            # Check if the API response indicates an error
            if weather_data.get("cod") != 200:
                print(f"Error: {weather_data.get('message', 'Unknown error')}")
                return None
            # Return the weather data dictionary
            return weather_data
        else:
            print("Could not connect to the weather service.")
            return None
    except requests.exceptions.RequestException:
        print("Could not establish a connection to the weather service.")
        return None

def display_weather(weather_data, units):
    """
    Display the weather forecast in a readable format.
    """
    if weather_data is None:
        return

    try:
        # Extract the relevant information from the weather data
        city = weather_data["name"]
        country_code = weather_data["sys"].get("country")

        # Display the city name and country code
        print(f"City: {city} ({country_code})")

        # Extract other weather information
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        max_temperature = weather_data["main"]["temp_max"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        wind_direction_deg = weather_data["wind"].get("deg")

        # Convert wind direction in degrees to compass direction
        wind_direction = get_wind_direction(wind_direction_deg)

        # Display the weather information with the appropriate units
        if units == "imperial":
            print(f"Temperature: {temp}°F")
            print(f"Feels Like: {feels_like}°F")
            print(f"Max Temperature: {max_temperature}°F")
            print(f"Wind Speed: {wind_speed} mph")
        else:
            print(f"Temperature: {temp}°C")
            print(f"Feels Like: {feels_like}°C")
            print(f"Max Temperature: {max_temperature}°C")
            print(f"Wind Speed: {wind_speed} m/s")

        print(f"Humidity: {humidity}%")
        print(f"Wind Direction: {wind_direction}")

    except KeyError:
        print("Error: Invalid weather data format.")

def get_wind_direction(degrees):
    """
    Convert wind direction in degrees to compass direction.
    Returns the compass direction as a string.
    """
    if degrees is None:
        return "Unknown"

    # Define the compass directions and their corresponding degree ranges
    directions = {
        "N": range(349, 11),
        "NNE": range(11, 34),
        "NE": range(34, 56),
        "ENE": range(56, 79),
        "E": range(79, 101),
        "ESE": range(101, 124),
        "SE": range(124, 146),
        "SSE": range(146, 169),
        "S": range(169, 191),
        "SSW": range(191, 214),
        "SW": range(214, 236),
        "WSW": range(236, 259),
        "W": range(259, 281),
        "WNW": range(281, 304),
        "NW": range(304, 326),
        "NNW": range(326, 349)
    }

    # Iterate through the compass directions and check if the degrees fall within the range
    for direction, degree_range in directions.items():
        if int(degrees) in degree_range:
            return direction

    return "Unknown"

def get_zip_or_city():
    """
    Prompt the user to enter a zip code or city name.
    Returns the user input.
    """
    return input("Enter a zip code or city name: ").strip()

def get_units():
    """
    Prompt the user to choose the units for displaying the weather.
    Returns the user's choice ("imperial" or "metric").
    """
    while True:
        units = input("Choose the units (imperial/metric): ").strip().lower()
        if units in ["imperial", "metric"]:
            return units
        else:
            print("Invalid choice. Please enter 'imperial' or 'metric'.")

def main():
    while True:
        zip_or_city = get_zip_or_city()
        units = get_units()

        # Validate if the user entered valid data (zip code or city name)
        if zip_or_city.isdigit():
            print("Fetching weather data by zip code...")
        else:
            print("Fetching weather data by city name...")

        weather_data = get_weather(zip_or_city, units)
        display_weather(weather_data, units)

        repeat = input("Do you want to check the weather again? (yes/no): ").strip().lower()
        if repeat not in ["yes", "y"]:
            break

if __name__ == "__main__":
    main()
