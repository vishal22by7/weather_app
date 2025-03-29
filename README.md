# Weather App

A simple application to display current weather and a 5-day forecast using the OpenWeatherMap API.

## Features

- Fetches current weather data for any city.
- Displays a 5-day weather forecast.
- Responsive and user-friendly interface.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/weather_app.git
   cd weather_app
   ```
2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate # For Linux/Mac
   venv\Scripts\activate # For Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Create a .env file in the root directory and add your OpenWeatherMap API key:
   OPENWEATHER_API_KEY=your_actual_api_key_here

  Note: Replace your_actual_api_key_here with your OpenWeatherMap API key.

5. Run the application:
   python app.py
