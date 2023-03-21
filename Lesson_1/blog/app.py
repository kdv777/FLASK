from time import time

from flask import Flask, request, g

app = Flask(__name__)


@app.route('/<string:city>', methods=['GET', 'POST'])
def index(city: str):
    name = request.args.get('name', None)
    return f"Hello, {city}! {request.method}", 201


@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()


@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time
    return response


