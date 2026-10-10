"""Bai 2: phan tich JSON va canh bao theo nguong."""
import json
import math
from mqtt_common import connection, listen, parser, run


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode('utf-8'))
        if not isinstance(data, dict) or data.get('device_id') != 'sensor01':
            raise ValueError('device_id phai la sensor01')
        temperature, humidity = data['temperature'], data['humidity']
        if any(isinstance(v, bool) or not isinstance(v, (int, float))
               or not math.isfinite(v) for v in (temperature, humidity)):
            raise ValueError('Nhiet do va do am phai la so huu han')
        if not 0 <= humidity <= 100:
            raise ValueError('Do am phai trong khoang 0..100')
    except (ValueError, KeyError, TypeError) as exc:
        print(f'Payload khong hop le: {exc}', flush=True)
        return
    print(f'\nDevice: {data["device_id"]}\nTemperature: {temperature} C\n'
          f'Humidity: {humidity} %', flush=True)
    if temperature > 35:
        print('CANH BAO: Nhiet do cao', flush=True)
    if humidity < 40:
        print('CANH BAO: Do am thap', flush=True)


def main():
    args = parser('Bai 2 - Monitoring Subscriber').parse_args()
    with connection(args, ['iot/lab/sensor01/data'], on_message):
        listen()


if __name__ == '__main__':
    run(main)
