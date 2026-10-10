"""Bai 1: nhan thong diep va in thoi diem nhan."""
from datetime import datetime
from mqtt_common import connection, listen, parser, run


def on_message(client, userdata, message):
    print(f'\nNhan duoc message:\nTopic: {message.topic}\n'
          f'Payload: {message.payload.decode("utf-8", errors="replace")}\n'
          f'Time: {datetime.now():%H:%M:%S}', flush=True)


def main():
    args = parser('Bai 1 - Subscriber').parse_args()
    with connection(args, ['iot/lab/message'], on_message):
        listen()


if __name__ == '__main__':
    run(main)
