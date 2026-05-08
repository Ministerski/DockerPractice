import os
import time
import random
import json
import paho.mqtt.client as mqtt


MQTT_HOST = os.getenv('SIM_HOST', '192.168.5.1') # IP брокера по умолчанию
MQTT_PORT = int(os.getenv('SIM_PORT', 1883))
SENSOR_TYPE = os.getenv('SIM_TYPE', 'temperature')
SENSOR_NAME = os.getenv('SIM_NAME', 'sensor_1')
INTERVAL = int(os.getenv('SIM_PERIOD', 5))

# Базовый класс
class Sensor:
    def __init__(self, name):
        self.name = name
    
    def get_value(self):
        pass

# 4 датчика
class TemperatureSensor(Sensor):
    def get_value(self):
        #(Август = 8)
        return round(random.uniform(2.0, 4.0) * 8.0, 2)

class PressureSensor(Sensor):
    def get_value(self):
        # Прибавляем 8 к базовому давлению
        return round(random.uniform(740.0, 760.0) + 8.0, 2)

class CurrentSensor(Sensor):
    def get_value(self):
        return round(random.uniform(1.0, 5.0) * 8.0, 2)

class VoltageSensor(Sensor):
    def get_value(self):
        return round(random.uniform(210.0, 230.0) + 8.0, 2)

def main():
    # Инициализация нужного типа датчика
    if SENSOR_TYPE == 'temperature':
        sensor = TemperatureSensor(SENSOR_NAME)
    elif SENSOR_TYPE == 'pressure':
        sensor = PressureSensor(SENSOR_NAME)
    elif SENSOR_TYPE == 'current':
        sensor = CurrentSensor(SENSOR_NAME)
    elif SENSOR_TYPE == 'voltage':
        sensor = VoltageSensor(SENSOR_NAME)
    else:
        sensor = Sensor(SENSOR_NAME)

    # Настройка MQTT клиента
    client = mqtt.Client(client_id=SENSOR_NAME)
    
    while True:
        try:
            client.connect(MQTT_HOST, MQTT_PORT, 60)
            print(f"Connected to Broker at {MQTT_HOST}:{MQTT_PORT}")
            break
        except Exception as e:
            print(f"Connection failed. Retrying in 5 sec...")
            time.sleep(5)

    client.loop_start()

    # Бесконечный цикл генерации и отправки данных
    while True:
        val = sensor.get_value()
        
        # Доп. задание: JSON формат топика
        topic = f"/sensor/{SENSOR_TYPE}"
        payload = json.dumps({"name": SENSOR_NAME, "value": val})
        
        client.publish(topic, payload)
        print(f"Published: {topic} -> {payload}")
        
        time.sleep(INTERVAL)

if __name__ == '__main__':
    main()