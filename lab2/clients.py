import hazelcast

client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=[
    "172.18.0.3:5701",
    "172.18.0.4:5701",
    "172.18.0.5:5701"
])
topic = client.get_topic("topic2").blocking()

def consume_messages():
    def on_message(message):
        print("The message is: ", message)
    topic.add_listener(on_message)
    while True:
        pass

#consume_messages()
queue = client.get_queue("Queue5").blocking()

def get_queue():
    while True:
        val  = queue.take()
        print("I get the following value: ", val)
        if(val == -1):
            queue.put(-1)
            break

get_queue()