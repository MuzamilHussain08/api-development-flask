from flask import Flask, request, jsonify
import json

app = Flask(__name__)

file = open("keys.json", "r")
keys = json.load(file)
file.close()


@app.route("/process", methods=["POST"])
def process():
    api_key = request.headers.get("X-API-Key")
    if api_key is None:
        return jsonify({"error": "API key is missing"}), 401
    
    found = False
    for name in keys:
        if keys[name] == api_key:
            found = True
            consumer = name

    if found == False:
        return jsonify({"error": "Invalid API key"}), 401

    data = request.get_json()
    if data is None or "text" not in data:
        return jsonify({"error": "Send JSON with a text field"}), 400

    result = data["text"].upper()
    return jsonify({"consumer": consumer, "result": result})


if __name__ == "__main__":
    app.run(debug=True)
