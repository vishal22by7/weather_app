from flask import Flask, request, render_template, redirect, url_for, flash, session
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Needed for flash and session

API_KEY = os.getenv('OPENWEATHER_API_KEY')
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'

def get_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        description = data['weather'][0]['description'].lower()
        if 'clear' in description:
            icon = 'wi-day-sunny'
            background = 'sunny-bg'
        elif 'cloud' in description:
            icon = 'wi-cloudy'
            background = 'cloudy-bg'
        elif 'rain' in description or 'drizzle' in description:
            icon = 'wi-rain'
            background = 'rainy-bg'
        elif 'snow' in description:
            icon = 'wi-snow'
            background = 'snowy-bg'
        elif 'thunder' in description:
            icon = 'wi-thunderstorm'
            background = 'stormy-bg'
        else:
            icon = 'wi-na'
            background = 'default-bg'
        # Convert sunrise and sunset timestamps to readable time
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': description,
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': icon,
            'background': background,
            'sunrise': sunrise,
            'sunset': sunset
        }
    return None

def get_forecast(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        # Get one forecast per day (every 24 hours, so we take every 8th entry since data is every 3 hours)
        forecast_list = []
        for i in range(0, 40, 8):  # 40 entries = 5 days, step by 8 for daily
            entry = data['list'][i]
            date = datetime.fromtimestamp(entry['dt']).strftime('%A')  # e.g., "Monday"
            temp = entry['main']['temp']
            description = entry['weather'][0]['description'].lower()
            if 'clear' in description:
                icon = 'wi-day-sunny'
            elif 'cloud' in description:
                icon = 'wi-cloudy'
            elif 'rain' in description or 'drizzle' in description:
                icon = 'wi-rain'
            elif 'snow' in description:
                icon = 'wi-snow'
            elif 'thunder' in description:
                icon = 'wi-thunderstorm'
            else:
                icon = 'wi-na'
            forecast_list.append({
                'day': date,
                'temp': temp,
                'description': description,
                'icon': icon
            })
        return forecast_list
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
        forecast = get_forecast(city) if weather else None
        if weather is None:
            flash(f"Could not find weather data for '{city}'. Please check the city name and try again.")
            session.pop('weather', None)
            session.pop('forecast', None)
        else:
            session['weather'] = weather
            session['forecast'] = forecast
        return redirect(url_for('home'))
    weather = session.pop('weather', None)
    forecast = session.pop('forecast', None)
    return render_template('index.html', weather=weather, forecast=forecast)

if __name__ == '__main__':
    app.run(debug=True)