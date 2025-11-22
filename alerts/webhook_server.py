from flask import Flask, request, jsonify
import json

app = Flask(__name__)

with open("alerts/config.json") as f:
    CONFIG = json.load(f)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data is None:
        return jsonify({"error": "No JSON Provided"}), 400

    print("Received alert:", data)

    # TODO: connect to your model later

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CONFIG["port"])

