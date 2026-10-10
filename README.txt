THUC HANH PYTHON MQTT

Broker: Eclipse Mosquitto local, localhost:1883.
Cai thu vien: python -m pip install -r requirements.txt
Chay broker: mosquitto -c mosquitto.conf -v

Moi bai mo hai terminal, chay chuong trinh nhan truoc:
Bai 1:
  python subscriber_bai1.py
  python publisher_bai1.py --name "Nguyen Van A" --student-id "B23DCCN001"
  Thay ten va ma sinh vien bang thong tin cua ban.
Bai 2:
  python monitor_subscriber_bai2.py
  python sensor_publisher_bai2.py
Bai 3:
  python device_bai3.py
  python controller_bai3.py
  Nhap ON/OFF de dieu khien, EXIT de thoat.

Ket qua khi chay voi broker: nhan loi chao kem thoi gian; nhan JSON cam bien
moi 3 giay va canh bao nhiet do >35, do am <40; den phan hoi JSON ON/OFF.
Ctrl+C de dung. Ho tro --host va --port tren tat ca chuong trinh.
Huong dan chi tiet va cau hinh broker Windows: README.md.
