from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from fetch_earthquake_data import fetch_earthquakes
from fetch_rainfall_data import fetch_rainfall

def create_app():
    app = Flask(__name__)
    from .routes import main
    app.register_blueprint(main)

    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_earthquakes, 'interval', minutes=10)
    scheduler.add_job(fetch_rainfall, 'interval', minutes=10)
    scheduler.start()

    return app