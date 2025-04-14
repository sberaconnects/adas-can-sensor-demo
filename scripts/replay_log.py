from visualizer.dashboard import CLIDashboard
import time
import csv
import os
import sys

# Import and run the helper FIRST before importing anything from src/
# autopep8: off
from path_helper import add_src_to_path
add_src_to_path()
# autopep8: on

# Now it's safe to import from `src/`


def replay_csv_log(file_path="data/demo_drive_log.csv", delay=1.0):
    if not os.path.exists(file_path):
        print(f"❌ Log file not found: {file_path}")
        return

    dashboard = CLIDashboard()

    with open(file_path, mode='r') as f:
        reader = csv.DictReader(f)
        print(f"📼 Replaying log: {file_path}")
        for row in reader:
            # Convert types
            data = {
                "speed_kph": int(row["speed_kph"]),
                "rpm": int(row["rpm"]),
                "distance_m": float(row["distance_m"]),
                "ttc": float(row["ttc"]),
                "fcw": row["fcw"].lower() == 'true',
                "timestamp": float(row["timestamp"])
            }

            dashboard.render(data)
            time.sleep(delay)


if __name__ == "__main__":
    replay_csv_log()
