import logging
import os
import signal
import sys
import threading
import time

from flask import Flask, jsonify, request
from werkzeug.serving import make_server

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

PORT = int(os.getenv("PORT", "8080"))
STU_ID = os.getenv("STU_ID", "220239")
STU_GROUP = os.getenv("STU_GROUP", "AC-576")
STU_VARIANT = os.getenv("STU_VARIANT", "13")


@app.before_request
def log_request():
    logger.info(
        "Request %s %s",
        request.method,
        request.path
    )


@app.route("/")
def home():
    return jsonify({
        "message": f"Hello, variant {STU_VARIANT}"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })

@app.route("/live")
def live():
    return jsonify({
        "status": "live"
    })

@app.route("/ready")
def ready():
    return jsonify({
        "status": "ready"
    })


class GracefulServer:

    def __init__(self):
        self.server = make_server(
            "0.0.0.0",
            PORT,
            app
        )
        self.thread = threading.Thread(
            target=self.server.serve_forever
        )

    def start(self):
        logger.info("Application started")
        logger.info("STU_ID=%s", STU_ID)
        logger.info("STU_GROUP=%s", STU_GROUP)
        logger.info("STU_VARIANT=%s", STU_VARIANT)

        self.thread.start()

    def shutdown(self, signum, frame):
        logger.info("Shutting down gracefully")

        time.sleep(1)

        self.server.shutdown()
        self.thread.join(timeout=30)

        logger.info("Graceful shutdown completed")

        os._exit(0)


if __name__ == "__main__":

    server = GracefulServer()

    signal.signal(signal.SIGTERM, server.shutdown)
    signal.signal(signal.SIGINT, server.shutdown)

    server.start()