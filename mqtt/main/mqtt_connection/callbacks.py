from mqtt.configs.broker_configs import mqtt_broker_configs

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'Conectado: {client}')
        client.subscribe(mqtt_broker_configs["TOPIC"])
    else:
        print(f'Erro ao conectar! codigo={rc}')


def on_subscribe(client, userdata, mid, granted_qos):
    print(f'inscrito em: {mqtt_broker_configs["TOPIC"]}')
    print(f'QOS: {granted_qos}')




