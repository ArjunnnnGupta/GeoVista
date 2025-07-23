from flask import Blueprint, jsonify,render_template
import json
import os

bp = Blueprint('routes', __name__)
@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/api/incidents')
def get_incidents():
    data = []

    rainfall_path = 'data/rainfall.json'
    forecast_path = 'data/forecast.json'
    earthquake_path = 'data/earthquakes.json'

    if os.path.exists(rainfall_path):
        with open(rainfall_path) as f:
            rainfall = json.load(f)
            for r in rainfall:
                r['type'] = 'rainfall'
            data.extend(rainfall)

    if os.path.exists(forecast_path):
        with open(forecast_path) as f:
            forecast = json.load(f)
            for fcast in forecast:
                fcast['type'] = 'forecast'
            data.extend(forecast)

    if os.path.exists(earthquake_path):
        with open(earthquake_path) as f:
            earthquakes = json.load(f)
            for eq in earthquakes:
                eq['type'] = 'earthquake'
            data.extend(earthquakes)

    return jsonify(data)
