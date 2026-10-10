"""Bai 2: mo phong cam bien gui JSON moi 3 giay."""
import json
import random
import time
from mqtt_common import connection, parser, publish, run


def main():
    args = parser('Bai 2 - Sensor Publisher').parse_args()
    with connection(args) as client:
        while True:
            payload = json.dumps({'device_id': 'sensor01',
                                  'temperature': round(random.uniform(20, 40), 1),
                                  'humidity': round(random.uniform(30, 80), 1)})
            publish(client, 'iot/lab/sensor01/data', payload)
            print(f'Da gui: {payload}', flush=True)
            time.sleep(3)


if __name__ == '__main__':
    run(main)
