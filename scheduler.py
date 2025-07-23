from apscheduler.schedulers.background import BackgroundScheduler
from fetch_earthquake_data import fetch_earthquakes
from fetch_rainfall_data import fetch_rainfall

def start_scheduler():
    scheduler = BackgroundScheduler()
    fetch_earthquakes()
    fetch_rainfall()
    scheduler.add_job(fetch_earthquakes, 'interval', minutes=10)
    scheduler.add_job(fetch_rainfall, 'interval', minutes=10)
    scheduler.start()
    print("⏱ Scheduler started.")
