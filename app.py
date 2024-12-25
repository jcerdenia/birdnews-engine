import threading

from dotenv import load_dotenv
from flask import Flask

from misc.decorators import require_auth

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return "We are live.", 200


@app.route("/ping", methods=["GET"])
def ping():
    return "Pong!", 200


@app.route("/run", methods=["POST"])
@require_auth
def run():
    from engine import main

    thread = threading.Thread(target=main)
    thread.start()

    return "Running.", 200
