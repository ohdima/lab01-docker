import logging
import os
import signal
import sys
import threading
import time

from flask import Flask, Response, jsonify, request
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
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

METRIC_PREFIX = "web13_"

http_requests_total = Counter(
    f"{METRIC_PREFIX}http_requests_total",
    "Total number of HTTP requests",
    ["method", "status"]
)

http_request_duration_seconds = Histogram(
    f"{METRIC_PREFIX}http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method"]
)

active_connections = Gauge(
    f"{METRIC_PREFIX}active_connections",
    "Number of active HTTP requests"
)


@app.before_request
def before_request():
    request.start_time = time.time()
    active_connections.inc()

    logger.info(
        "Request %s %s",
        request.method,
        request.path
    )


@app.after_request
def after_request(response):
    duration = time.time() - request.start_time

    http_requests_total.labels(
        method=request.method,
        status=str(response.status_code)
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method
    ).observe(duration)

    active_connections.dec()

    return response


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


@app.route("/error")
def error():
    return jsonify({
        "error": "Simulated server error"
    }), 500


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


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
        logger.info("METRIC_PREFIX=%s", METRIC_PREFIX)

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