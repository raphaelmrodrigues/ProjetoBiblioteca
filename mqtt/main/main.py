from mqtt.configs.broker_configs import mqtt_broker_configs
from .mqtt_connection.mqtt_cient_connection import MqttClientConnection
import time


def start():
    mqtt_client_connection = MqttClientConnection(
        mqtt_broker_configs["HOST"],
        mqtt_broker_configs["PORT"],
        mqtt_broker_configs["CLIENT_NAME"],
        mqtt_broker_configs["KEEPALIVE"]
    )
    mqtt_client_connection.start_connection()




