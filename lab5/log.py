import hazelcast
import subprocess, signal
from flask import Flask, request
import argparse, uuid, json
import argparse

import consul, os

app = Flask(__name__)

port_parser = argparse.ArgumentParser()
port_parser.add_argument("--port", type=int, required=True)
args = port_parser.parse_args()

host_consul = "127.0.0.1"
port_consul = 8500
client_consul = consul.Consul(host=host_consul, port=port_consul)

def get_hazelcast_setup():
  _, hazelcastsettings = client_consul.kv.get("hazelcast_settings")
  return json.loads(hazelcastsettings['Value'])




hazelcast_settings = get_hazelcast_setup()


client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=[
    "172.18.0.3:5701",
  "172.18.0.4:5701",
  "172.18.0.5:5701",
])
message_store_map = hazelcast_settings["map_name"]
message_store = client.get_map(message_store_map).blocking()

def register_service(name, port):
  #id = 1
  id = str(uuid.uuid4())
  ip = os.getenv('SERVICE_IP', 'localhost')
  client_consul.agent.service.register(
    name,
    service_id=id,
    address=ip,
    port=port
  )


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
    print("ID: ", message_id, " The message is: ", message_content)
    # Validate presence of required data
    if not message_id or not message_content:
      return "Missing required data (id or message)", 400


    # Print received message for debugging
    print(f"Received message: {message_content}")

    return "Success"

  # Check for GET request to retrieve messages
  elif request.method == "GET":
    values = message_store.key_set()
    print(values)
    for val in values:
      buf = []
      res = message_store.get(val)
      buf.append(val)
      buf.append(res)
      results.append(buf)
    return results


  # Handle unsupported methods with a 400 error
  else:
    return "Unsupported request method", 400

# Run the application if executed directly
if __name__ == "__main__":
  register_service("log-service", args.port)
  app.run(port=args.port, debug=True)