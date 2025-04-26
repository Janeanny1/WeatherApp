"""
Weather Application Backend
Flask API for weather data with MySQL integration
"""

from flask import Flask, jsonify, g
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db():
    """
    Establishes and returns a database connection.
    Stores the connection in Flask's application context.
    """
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host="localhost",
                user="weather_user",
                password="123456789",
                database="weather_app",
                autocommit=True
            )
        except Error as e:
            app.logger.error("Database connection failed: %s", e)
            raise
    return g.db

@app.teardown_appcontext
def close_db(exception=any):  # Renamed 'e' to 'exception' for clarity
    """
    Closes the database connection at the end of the request.
    The exception parameter is required by Flask's teardown mechanism.
    """
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()

@app.route('/api/locations', methods=['GET'])
def get_saved_locations():
    """
    Retrieve all saved locations from the database.
    Returns JSON response with locations data or error message.
    """
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM saved_locations ORDER BY created_at DESC")
        locations = cursor.fetchall()
        return jsonify({
            "success": True,
            "data": locations,
            "count": len(locations)
        })       
    except Error as e:
        app.logger.error("Database error: %s", e)
        return jsonify({
            "success": False,
            "error": "Database operation failed",
            "details": str(e)
        }), 500  
    except Exception as e:  # pylint: disable=broad-except
        app.logger.error("Unexpected error: %s", e)
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)