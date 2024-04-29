import hazelcast
import subprocess, signal
import argparse
from flask import Flask, request

app = Flask(__name__)

port_parser = argparse.ArgumentParser()
port_parser.add_argument("--port", type=int, required=True)
args = port_parser.parse_args()

#p = subprocess.Popen(['./hazelcast.sh'])
client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=[
    "172.18.0.3:5701",
  "172.18.0.4:5701",
  "172.18.0.5:5701",
])

message_store = client.get_map("messages").blocking()

results = []
# Route decorator for handling log requests
@app.route("/log", methods=["POST", "GET"])
def handle_log():
  # Check for POST request to log a message
  if request.method == "POST":
    # Extract message id and content from form data
    message_id = request.form.get("id")
    message_content = request.form.get("msg")
    message_store.put(message_id,message_content)
    # Validate presence of required data
    if not message_id or not message_content:
      return "Missing required data (id or message)", 400


    # Print received message for debugging
    print(f"Received message: {message_content}")

    return "Success"

  # Check for GET request to retrieve messages
  elif request.method == "GET":
    values = message_store.key_set()
    for val in values:
      res = message_store.get(val)
      results.append(res)
    return results


  # Handle unsupported methods with a 400 error
  else:
    return "Unsupported request method", 400

# Run the application if executed directly
if __name__ == "__main__":
  app.run(port=args.port)