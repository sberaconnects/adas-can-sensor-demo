import can
from struct import unpack


class CANInterface:
    def __init__(self, channel='vcan0'):
        self.channel = channel
        self.bus = can.interface.Bus(channel=self.channel, bustype='socketcan')

    def receive(self, timeout=1.0):
        """
        Wait for and receive a CAN frame. Returns parsed sensor data.
        """
        msg = self.bus.recv(timeout)
        if msg is None:
            return None

        if msg.arbitration_id == 0x101 and len(msg.data) >= 6:
            return self.parse_sensor_data(msg.data)
        else:
            print(f"Received unrelated CAN frame: ID={msg.arbitration_id}")
            return None

    def parse_sensor_data(self, data):
        """
        Parse sensor CAN data into speed, RPM, and distance
        Data format: [speed (2 bytes), rpm (2 bytes), distance_cm (2 bytes), padding (2 bytes)]
        """
        speed, rpm, dist_cm = unpack('>HHH', data[:6])  # big endian
        distance = dist_cm / 100.0  # Convert cm to meters
        return {
            "speed_kph": speed,
            "rpm": rpm,
            "distance_m": distance
        }
