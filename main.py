from flask import Flask
from app.routes import main
from scheduler import start_scheduler

app = Flask(__name__)
app.register_blueprint(main)

start_scheduler()

if __name__ == "__main__":
    app.run(debug=True)
