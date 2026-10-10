"""Bai 1: gui loi chao kem thong tin sinh vien."""
import time
from mqtt_common import connection, parser, publish, run


def main():
    cli = parser('Bai 1 - Publisher')
    cli.add_argument('--name', required=True, help='Ho ten sinh vien')
    cli.add_argument('--student-id', required=True, help='Ma sinh vien')
    cli.add_argument('--message', default='Xin chao tu client Python MQTT')
    cli.add_argument('--count', type=int, default=1)
    args = cli.parse_args()
    if args.count < 1:
        cli.error('--count phai >= 1')
    payload = f'{args.message} - {args.student_id} - {args.name}'
    with connection(args) as client:
        for index in range(args.count):
            publish(client, 'iot/lab/message', payload)
            print(f'Da gui: {payload}')
            if index < args.count - 1:
                time.sleep(1)


if __name__ == '__main__':
    run(main)
