from waitress import serve
from flask import Flask
from flask import request


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    print("Server listening localhost:8080...")
    app.run("0.0.0.0", port=8080)
    # serve(app, host="0.0.0.0", port=8080, threads=4)
