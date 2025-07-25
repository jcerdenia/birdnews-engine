import threading

from flask import Flask

from config import Config
from engine import Engine
from misc.decorators import require_auth

app = Flask(__name__)


def main():
    config = Config.from_env()
    engine = Engine.from_config(config)
    engine.run()


@app.route("/", methods=["GET"])
def root():
    return "We are live.", 200


@app.route("/ping", methods=["GET"])
def ping():
    return "Pong!", 200


@app.route("/run", methods=["POST"])
@require_auth
def run():
    thread = threading.Thread(target=main)
    thread.start()

    return "Running.", 200
