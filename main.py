from flask import Flask
from app.routes import bp
from scheduler import start_scheduler

app = Flask(__name__)
app.register_blueprint(bp)

@app.before_first_request
def activate_scheduler():
    start_scheduler()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
