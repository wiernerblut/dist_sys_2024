from flask import Flask, request, abort, jsonify
import requests
import uuid

app = Flask(__name__)

logging_service_url = "http://localhost:5002/log"
messages_service_url = "http://localhost:5001/message"

@app.route("/", methods=["POST", "GET"])
def handle_request():
    if request.method == "POST":
        return handle_post_request()
    elif request.method == "GET":
        return handle_get_request()
    else:
        abort(400)

def handle_post_request():
    msg = request.form.get("msg")
    if not msg:
        return jsonify({"error": "Message not provided"}), 400
    unique_id = str(uuid.uuid4())
    data = {"id": unique_id, "msg": msg}
    response = requests.post(logging_service_url, data=data)
    if response.status_code == 200:
        return jsonify({"id": unique_id, "msg": msg}), 200
    else:
        return jsonify({"error": "Failed to log message"}), 500

def handle_get_request():
    log_response = requests.get(logging_service_url)
    msg_response = requests.get(messages_service_url)
    if log_response.status_code == 200 and msg_response.status_code == 200:
        return jsonify({"log_messages": log_response.text, "other_messages": msg_response.text}), 200
    else:
        return jsonify({"error": "Failed to retrieve messages"}), 500

if __name__ == "__main__":
    app.run(port=5000)
