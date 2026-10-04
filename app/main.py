"""A tiny Flask microservice used to demonstrate containerisation,
CI/CD and deployment on AWS (ECR + EC2)."""
import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "1.0.0")


@app.route("/")
def index():
    return jsonify(
        message="Hello from the cloud microservice!",
        version=VERSION,
    )


@app.route("/health")
def health():
    """Used by load balancers / monitors to check the service is alive."""
    return jsonify(status="ok"), 200


@app.route("/hello/<name>")
def hello(name):
    return jsonify(message=f"Hello, {name}!")


@app.route("/info")
def info():
    """Shows which container/host served the request (useful to demo scaling)."""
    return jsonify(
        hostname=socket.gethostname(),
        time_utc=datetime.now(timezone.utc).isoformat(),
        version=VERSION,
    )


@app.route("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify(a=a, b=b, result=a + b)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
