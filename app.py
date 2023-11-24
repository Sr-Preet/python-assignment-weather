from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)

def get_weather_data(city, units='metric'):
    # Set the URL for the OpenWeatherMap API
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Create a dictionary to store the parameters for the API request
    params = {
        'q': city,
        'appid': 'a771e288754956cacb9456ec050c7e94',
        'units': units
    }

    try:
        # Make a GET request to the API using the requests library
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Convert the JSON response to a Python dictionary
        data = response.json()

        # Extract the required data from the dictionary
        city = data['name']
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Get the current date and day
        now = datetime.now()
        current_date = now.strftime("%d %b %Y")
        current_day = now.strftime("%A")

        return {
            'city': city,
            'temperature': temperature,
            'description': description,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'current_date': current_date,
            'current_day': current_day,
            'units': units
        }

    except requests.exceptions.HTTPError as err:
        print(f"Error fetching data from OpenWeatherMap API: {err}", 'error')
        return None
    except requests.exceptions.RequestException as err:
        print(f"Error connecting to OpenWeatherMap API: {err}", 'error')
        return None
    except KeyError as err:
        print(f"Error parsing OpenWeatherMap API response: {err}", 'error')
        return None

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route("/weatherapp", methods=["POST", "GET"])
def get_weatherdata():
    if request.method == 'POST':
        city = request.form.get("city")
        units = request.form.get("units", "metric")  # Default to metric if not provided

        weather_data = get_weather_data(city, units)

        if weather_data:
            return render_template('response.html', **weather_data)

    return render_template('response.html', city=None, temperature=None, description=None, humidity=None, wind_speed=None, current_date=None, current_day=None)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
