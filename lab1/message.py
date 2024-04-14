from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/message", methods=["GET"])
def get_message():
  return jsonify({"message": "Coming soon"}), 200

if __name__ == "__main__":
  app.run(port=5001)
