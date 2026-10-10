"""Bai 3: nhap lenh dieu khien va nhan phan hoi tu den."""
import json
import threading
from mqtt_common import connection, parser, publish, run


def main():
    args = parser('Bai 3 - Controller App').parse_args()
    response = threading.Event()
    expected = [None]

    def on_message(client, userdata, message):
        try:
            data = json.loads(message.payload.decode('utf-8'))
            if (not isinstance(data, dict) or data.get('device_id') != 'light01'
                    or data.get('status') not in ('ON', 'OFF')):
                raise ValueError('Trang thai den khong hop le')
        except (ValueError, TypeError) as exc:
            print(f'Payload khong hop le: {exc}', flush=True)
            return
        print('\nTrang thai nhan duoc:\n' + json.dumps(data), flush=True)
        if data['status'] == expected[0]:
            response.set()

    with connection(args, ['iot/lab/light01/status'], on_message) as client:
        while True:
            command = input('Nhap lenh (ON/OFF/EXIT): ').strip().upper()
            if command == 'EXIT':
                break
            if command not in ('ON', 'OFF'):
                print('Lenh sai. Chi nhap ON, OFF hoac EXIT.')
                continue
            expected[0] = command
            response.clear()
            publish(client, 'iot/lab/light01/cmd', command)
            print(f'Da gui lenh {command} toi light01', flush=True)
            if not response.wait(5):
                print('Chua nhan phan hoi. Kiem tra device_bai3.py dang chay.')


if __name__ == '__main__':
    run(main)
