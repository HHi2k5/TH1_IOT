"""Kiem tra nguong canh bao va phan hoi lenh, khong can broker."""
import contextlib
import io
import json
from types import SimpleNamespace
import unittest

import monitor_subscriber_bai2 as monitor
import device_bai3 as device


class LabTests(unittest.TestCase):
    def test_warning_boundaries(self):
        for temperature, humidity, hot, dry in (
                (36.1, 38.7, True, True), (35, 40, False, False),
                (36, 50, True, False), (25, 30, False, True)):
            with self.subTest(temperature=temperature, humidity=humidity):
                output = io.StringIO()
                payload = json.dumps(dict(device_id='sensor01',
                                          temperature=temperature, humidity=humidity))
                with contextlib.redirect_stdout(output):
                    monitor.on_message(None, None, SimpleNamespace(payload=payload.encode()))
                self.assertEqual('Nhiet do cao' in output.getvalue(), hot)
                self.assertEqual('Do am thap' in output.getvalue(), dry)

    def test_invalid_sensor_payload(self):
        for payload in (b'[]', b'invalid', b'{}', b'\xff',
                        b'{"device_id":"sensor01","temperature":true,"humidity":50}'):
            with self.subTest(payload=payload):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    monitor.on_message(None, None, SimpleNamespace(payload=payload))
                self.assertIn('Payload khong hop le', output.getvalue())

    def test_light_commands(self):
        sent = []

        def publish(topic, payload, qos):
            sent.append((topic, json.loads(payload), qos))
            return SimpleNamespace(rc=0)

        client = SimpleNamespace(publish=publish)
        with contextlib.redirect_stdout(io.StringIO()):
            for command in (b'ON', b'OFF', b'BAD'):
                device.on_message(client, None, SimpleNamespace(payload=command))
        self.assertEqual(sent, [
            ('iot/lab/light01/status', {'device_id': 'light01', 'status': 'ON'}, 1),
            ('iot/lab/light01/status', {'device_id': 'light01', 'status': 'OFF'}, 1)])


if __name__ == '__main__':
    unittest.main()
