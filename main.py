from flask import Flask
from app.routes import bp
from scheduler import start_scheduler

app = Flask(__name__)
app.register_blueprint(bp)

start_scheduler()

if __name__ == "__main__":
    app.run(debug=True)