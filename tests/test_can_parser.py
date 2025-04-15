from canbus.can_interface import CANInterface


def test_parse_sensor_data():
    interface = CANInterface()
    # Simulate bytes: speed=100 (0x0064), rpm=3000 (0x0BB8), dist=25.00m (0x09C4 = 2500 cm)
    frame = bytes.fromhex("00640BB809C40000")
    result = interface.parse_sensor_data(frame)

    assert result["speed_kph"] == 100
    assert result["rpm"] == 3000
    assert abs(result["distance_m"] - 25.0) < 0.01
