import hazelcast

client = hazelcast.HazelcastClient(cluster_name="dev", cluster_members=[
    "172.18.0.3:5701",
    "172.18.0.4:5701",
    "172.18.0.5:5701"
])
#map = client.get_map("IMapLab2_one_node").blocking()
def task1():
    counter = 0
    key_str = "key1"
    key = 0
    for i in range(1000):
        key += 1
        counter += 1
        #print(map.put(key,counter))
        map.put("Key " + str(key),counter)

#task1()
topic = client.get_topic("topic2").blocking()
def task2():
    for i in range(0,100):
        print("Message: ", i)
        topic.publish(i)
        print()
    print("Published")
#task2()

queue = client.get_queue("Queue5").blocking()

def task3():
    for i in range(0,100):
        queue.put(i)
        print("Number in queue ", i)
    queue.put(-1)
    print("Finished to write into the queue")
'''
ertretetrret
'''
task3()