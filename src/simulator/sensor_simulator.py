import random
import time
import can


class SensorSimulator:
    def __init__(self, channel='vcan0', bitrate=500000):
        self.bus = can.interface.Bus(channel=channel, bustype='socketcan')

    def generate_sensor_data(self):
        # Simulate realistic vehicle values
        speed_kph = random.randint(40, 120)
        rpm = random.randint(1500, 4000)
        distance_m = random.uniform(5.0, 50.0)
        return speed_kph, rpm, distance_m

    def pack_data(self, speed, rpm, distance):
        # Convert data to bytes for CAN payload (8 bytes total)
        speed_bytes = speed.to_bytes(2, 'big')       # 2 bytes
        rpm_bytes = rpm.to_bytes(2, 'big')           # 2 bytes
        dist_bytes = int(distance * 100).to_bytes(2,
                                                  # 2 bytes (cm precision)
                                                  'big')

        padding = bytes(2)  # Remaining 2 bytes unused
        return speed_bytes + rpm_bytes + dist_bytes + padding

    def send(self):
        while True:
            speed, rpm, distance = self.generate_sensor_data()
            data = self.pack_data(speed, rpm, distance)

            msg = can.Message(arbitration_id=0x101,
                              data=data, is_extended_id=False)

            try:
                self.bus.send(msg)
                print(
                    f"Sent: Speed={speed} km/h | RPM={rpm} | Distance={distance:.2f} m")
            except can.CanError:
                print("❌ Message NOT sent")

            time.sleep(1)


if __name__ == "__main__":
    simulator = SensorSimulator()
    simulator.send()
