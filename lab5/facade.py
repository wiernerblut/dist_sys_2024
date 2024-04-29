from flask import Flask, request, abort, jsonify
import requests, json
import uuid
import random
import hazelcast
import consul, os

app = Flask(__name__)

host_consul = "127.0.0.1"
port_consul = 8500
client_consul = consul.Consul(host=host_consul, port=port_consul)
def get_service_address(name):
    _, services = client_consul.catalog.service(name)
    if services:
        address = services[0]['ServiceAddress']
        port = services[0]['ServicePort']
        return f"http://{address}:{port}"

def get_hazelcast_setup():
    _, hazelcastsettings = client_consul.kv.get("hazelcast_settings")
    return json.loads(hazelcastsettings['Value'])



def get_msg_queue_setup():
    _, mapsettings = client_consul.kv.get("message_queue_settings")
    return json.loads(mapsettings['Value'])


def register_service(name, port):
    id = str(uuid.uuid4())
    ip = os.getenv('SERVICE_IP', 'localhost')
    client_consul.agent.service.register(
        name,
        service_id=id,
        address=ip,
        port=port
    )


logging_service_address = get_service_address("log-service")
messages_service_address = get_service_address("messages-service")



#logging_service_url = "http://localhost:5002/log"
#messages_service_url = "http://localhost:5001/message"
client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=[
    "172.18.0.3:5701",
  "172.18.0.4:5701",
  "172.18.0.5:5701",
])

hazelcast_settings = get_hazelcast_setup()
message_queue_settings = get_msg_queue_setup()
message_queue = message_queue_settings["queue_name"]
queue = client.get_queue(message_queue).blocking()

@app.route("/", methods=["POST", "GET"])
def handle_request():
    if request.method == "POST":
        return handle_post_request()
    elif request.method == "GET":
        return handle_get_request()
    else:
        abort(400)

def handle_post_request():
    port = random.randint(5000, 5002)
    print("port: ", port)
    msg = request.form.get("msg")
    if not msg:
        return jsonify({"error": "Message not provided"}), 400
    unique_id = str(uuid.uuid4())
    data = {"id": unique_id, "msg": msg}
    print(data)
    response = requests.post("http://localhost:{}/log".format(port), data=data)
    queue.offer(json.dumps(msg))
    if response.status_code == 200:
        return jsonify({"id": unique_id, "msg": msg}), 200
    else:
        return jsonify({"error": "Failed to log message"}), 500

def handle_get_request():
    port = random.randint(5000, 5002)
    print(port)
    port2 = random.randint(5003, 5004)
    print(port2)
    log_response = requests.get("http://localhost:{}/log".format(port))
    msg_response = requests.get("http://localhost:{}/message".format(port2))
    #msg_response = requests.get(messages_service_url)
    if log_response.status_code == 200 and msg_response.status_code == 200:
        return jsonify({"log_messages": log_response.text, "msg": msg_response.text}), 200
    else:
        return jsonify({"error": "Failed to retrieve messages"}), 500

if __name__ == "__main__":
    app.run(port=4999, debug=True)