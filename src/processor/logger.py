import csv
import os


class ADASLogger:
    def __init__(self, filename="data/demo_drive_log.csv"):
        self.filename = filename
        self.headers = ['timestamp', 'speed_kph',
                        'rpm', 'distance_m', 'ttc', 'fcw']
        self._init_log()

    def _init_log(self):
        # Create file with headers if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def log(self, data):
        with open(self.filename, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow({
                'timestamp': round(data['timestamp'], 2),
                'speed_kph': data['speed_kph'],
                'rpm': data['rpm'],
                'distance_m': round(data['distance_m'], 2),
                'ttc': round(data['ttc'], 2),
                'fcw': data['fcw']
            })
