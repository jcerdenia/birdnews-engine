import threading

from dotenv import load_dotenv
from flask import Flask

from engine import Engine
from misc.decorators import require_auth

app = Flask(__name__)

load_dotenv()


@app.route("/", methods=["GET"])
def root():
    return "We are live.", 200


@app.route("/ping", methods=["GET"])
def ping():
    return "Pong!", 200


@app.route("/run", methods=["POST"])
@require_auth
def run():
    def task():
        engine = Engine()
        engine.run()

    thread = threading.Thread(target=task)
    thread.start()

    return "Running.", 200


@app.route("/sweep", methods=["POST"])
@require_auth
def sweep():
    def task():
        engine = Engine()
        engine.sweep_duplicates()

    thread = threading.Thread(target=task)
    thread.start()

    return "Sweeping.", 200
