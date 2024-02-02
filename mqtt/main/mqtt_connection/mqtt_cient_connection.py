import paho.mqtt.client as mqtt
from .callbacks import on_connect, on_subscribe

class MqttClientConnection:
    def __init__(self, broker_ip: str, port: int, client_name: str, keepalive=60):
        self.__broker_ip = broker_ip
        self.__port = port
        self.__client_name = client_name
        self.__keepalive = keepalive
        self.last_message = None
        self.__connected = False

    def start_connection(self):
        mqtt_client = mqtt.Client(self.__client_name)

        mqtt_client.on_connect = on_connect
        mqtt_client.on_subscribe = on_subscribe
        mqtt_client.on_message = self.on_message


        mqtt_client.connect(host=self.__broker_ip, port=self.__port, keepalive=self.__keepalive)
        self.__mqtt_client = mqtt_client
        self.__mqtt_client.loop_start()
        self.__connected = True


    def on_message(self, client, userdata, message):
        print('Mensagem recebida!')
        print(client)
        print(message.payload)
        self.last_message = message.payload.decode('utf-8')

    def get_last_message(self):
        return self.last_message

    def end_connection(self):
        try:
            self.__mqtt_client.loop_stop()
            self.__mqtt_client.disconnect()
            print("Desconectado do broker MQTT com sucesso.")
            return True
        except Exception as e:
            print(f"Falha ao desconectar do broker MQTT. Erro: {e}")
            return False


    def is_connected(self):
        return self.__connected