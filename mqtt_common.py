"""Cau hinh va vong doi MQTT dung chung cho ba bai."""
import argparse
from contextlib import contextmanager
import threading
import time

import paho.mqtt.client as mqtt


def parser(description):
    result = argparse.ArgumentParser(description=description)
    result.add_argument('--host', default='localhost', help='Dia chi MQTT broker')
    result.add_argument('--port', type=int, default=1883)
    return result


@contextmanager
def connection(args, topics=(), on_message=None):
    ready = threading.Event()
    errors = []
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect_timeout = 10

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            errors.append(f'Broker tu choi ket noi: {reason_code}')
            ready.set()
            return
        print(f'Da ket noi broker {args.host}:{args.port}', flush=True)
        if topics:
            result, _ = client.subscribe([(topic, 1) for topic in topics])
            if result != mqtt.MQTT_ERR_SUCCESS:
                errors.append('Khong the dang ky topic')
                ready.set()
        else:
            ready.set()

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        if any(code.is_failure for code in reason_codes):
            errors.append('Broker tu choi subscribe')
        else:
            print('Dang lang nghe: ' + ', '.join(topics), flush=True)
        ready.set()

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    try:
        client.connect(args.host, args.port, keepalive=60)
        client.loop_start()
        if not ready.wait(10):
            raise TimeoutError('Het thoi gian cho ket noi/subscribe broker')
        if errors:
            raise RuntimeError(errors[0])
        yield client
    finally:
        client.disconnect()
        client.loop_stop()


def publish(client, topic, payload):
    info = client.publish(topic, payload, qos=1)
    if info.rc != mqtt.MQTT_ERR_SUCCESS:
        raise RuntimeError(f'Gui MQTT that bai: {mqtt.error_string(info.rc)}')
    info.wait_for_publish(timeout=10)
    if not info.is_published():
        raise TimeoutError('Broker chua xac nhan thong diep')


def listen():
    while True:
        time.sleep(1)


def run(main):
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nDa dung chuong trinh.')
    except (OSError, RuntimeError, ValueError) as exc:
        raise SystemExit(f'Loi: {exc}') from exc
