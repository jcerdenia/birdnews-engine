import os
import threading

from dotenv import load_dotenv
from flask import Flask

from engine import Engine
from misc.decorators import require_auth

app = Flask(__name__)

load_dotenv()


def main():
    engine = Engine()
    engine.run()


@app.route("/ping", methods=["GET"])
def ping():
    return "Pong!", 200


@app.route("/run", methods=["POST"])
@require_auth
def run():
    thread = threading.Thread(target=main)
    thread.start()

    return "Running.", 200


if __name__ == "__main__":
    app.run(debug=True)
