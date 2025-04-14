import time


class ADASProcessor:
    def __init__(self, ttc_threshold=2.0):
        self.ttc_threshold = ttc_threshold

    def compute_ttc(self, speed_kph, distance_m):
        speed_mps = speed_kph / 3.6  # Convert to meters per second
        if speed_mps <= 0:
            return float('inf')  # Avoid division by zero
        return distance_m / speed_mps

    def check_fcw(self, sensor_data):
        speed = sensor_data['speed_kph']
        distance = sensor_data['distance_m']

        ttc = self.compute_ttc(speed, distance)
        fcw = ttc < self.ttc_threshold

        # Debug info
        print(
            f"🚘 TTC: {ttc:.2f}s | Threshold: {self.ttc_threshold:.1f}s | FCW: {'YES' if fcw else 'NO'}")

        return {
            'ttc': round(ttc, 2),
            'fcw': fcw,
            'timestamp': time.time(),
            **sensor_data
        }
