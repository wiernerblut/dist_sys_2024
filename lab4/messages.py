import hazelcast
import subprocess, signal
import argparse
from flask import Flask, request, jsonify

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

message_queue = "message_queue_lab4"
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
    app.run(port=args.port)