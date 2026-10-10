"""Bai 3: den light01 nhan lenh va phan hoi trang thai."""
import json
from mqtt_common import connection, listen, parser, run


def on_message(client, userdata, message):
    command = message.payload.decode('utf-8', errors='replace').strip()
    if command not in ('ON', 'OFF'):
        print(f'Lenh khong hop le: {command!r}', flush=True)
        return
    payload = json.dumps({'device_id': 'light01', 'status': command})
    # Khong wait_for_publish trong callback: callback chay tren network thread.
    info = client.publish('iot/lab/light01/status', payload, qos=1)
    if info.rc != 0:
        print(f'Khong the gui trang thai: {info.rc}', flush=True)
    else:
        print(f'Trang thai den: {command}', flush=True)


def main():
    args = parser('Bai 3 - Smart Light Device').parse_args()
    with connection(args, ['iot/lab/light01/cmd'], on_message):
        listen()


if __name__ == '__main__':
    run(main)
