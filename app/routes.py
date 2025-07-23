from flask import Blueprint, render_template, jsonify
import json, os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/incidents')
def incidents():
    data = []
    for fn in ["data/earthquakes.json", "data/rainfall.json"]:
        if os.path.exists(fn):
            with open(fn) as f:
                data.extend(json.load(f))
    return jsonify(data)
