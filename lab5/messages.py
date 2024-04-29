import hazelcast
import subprocess, signal
import argparse
from flask import Flask, request, jsonify
import consul, os
import argparse, uuid, json

app = Flask(__name__)

port_parser = argparse.ArgumentParser()
port_parser.add_argument("--port", type=int, required=True)
args = port_parser.parse_args()

host_consul = "127.0.0.1"
port_consul = 8500
client_consul = consul.Consul(host=host_consul, port=port_consul)

def register_service(service_name, service_port):
  service_id = str(uuid.uuid4())
  service_ip = os.getenv('SERVICE_IP', 'localhost')
  client_consul.agent.service.register(
    service_name,
    service_id=service_id,
    address=service_ip,
    port=service_port
  )

def get_message_queue_settings():
    _, hazelcastsettings = client_consul.kv.get("message_queue_settings")
    return json.loads(hazelcastsettings['Value'])


#p = subprocess.Popen(['./hazelcast.sh'])
client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=[
    "172.18.0.3:5701",
  "172.18.0.4:5701",
  "172.18.0.5:5701",
])
message_queue_settings = get_message_queue_settings()
message_queue = message_queue_settings["queue_name"]
queue = client.get_queue(message_queue).blocking()

messages_array = []

@app.route("/message", methods=["GET"])
def get_message():
    for i in range(0,5):
        var = queue.take()
        print(var)
        if (i==5):
            break
        messages_array.append(var)
    return jsonify({"message": messages_array}), 200

if __name__== "__main__":
    register_service("messages-service", args.port)
    app.run(port=args.port)