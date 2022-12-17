from awsiot import mqtt_connection_builder, mqtt
import os
import time
client_id = "SWIRE-SDK-95"

ROOT_DIR = os.getcwd()

topic_name = "andy_testing_this_topic"

end_point = "afqs0qlhy6qg3-ats.iot.ap-southeast-1.amazonaws.com"

mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint="afqs0qlhy6qg3-ats.iot.ap-southeast-1.amazonaws.com",
        cert_filepath=ROOT_DIR + "/cert/SWIRE-SDK-95.pem",
        pri_key_filepath=ROOT_DIR + "/key_private/SWIRE-SDK-95.pem.key",
        ca_filepath=ROOT_DIR + "/rootca/AmazonRootCA1.pem",
        client_id=client_id,
        keep_alive_secs=60
    )

def on_receive_message(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))

def publish_one_message_per_second():
    current_number = 0
    while True:
        current_number += 1
        mqtt_connection.publish(
            topic=topic_name,
            payload=f"just a testing message {current_number}",
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        time.sleep(1)

if __name__ == '__main__':
    # publish_one_message_per_second()
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print(f'{client_id} is connected!')
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=topic_name,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_receive_message
    )
    publish_one_message_per_second()
   
