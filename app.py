from flask import Flask, jsonify, request, send_from_directory
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def serve_frontend():
    """Serve the main frontend HTML file"""
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (JS, CSS, etc.)"""
    return send_from_directory('static', path)

@app.route('/api/weather')
def get_weather():
    """Fetch weather data from MetaWeather API"""
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location parameter is required"}), 400
    
    try:
        # Step 1: Get location WOEID
        search_response = requests.get(
            f"https://www.metaweather.com/api/location/search/?query={location}",
            timeout=10
        )
        search_response.raise_for_status()
        location_data = search_response.json()
        
        if not location_data:
            return jsonify({"error": "Location not found"}), 404
            
        woeid = location_data[0]['woeid']
        
        # Step 2: Get weather data
        weather_response = requests.get(
            f"https://www.metaweather.com/api/location/{woeid}/",
            timeout=10
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Extract current weather (first in consolidated_weather array)
        current_weather = weather_data['consolidated_weather'][0]
        
        return jsonify({
            "city": weather_data['title'],
            "temperature": round(current_weather['the_temp'], 1),
            "conditions": current_weather['weather_state_name'],
            "humidity": current_weather['humidity'],
            "wind_speed": round(current_weather['wind_speed'], 1),
            "icon": f"https://www.metaweather.com/static/img/weather/{current_weather['weather_state_abbr']}.svg"
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Weather API request failed",
            "details": str(e)
        }), 500
    except (KeyError, IndexError) as e:
        return jsonify({
            "error": "Unexpected weather data format",
            "details": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)