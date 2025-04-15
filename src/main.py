import matplotlib.pyplot as plt
import argparse
import time
import csv
import os
import threading

from canbus.can_interface import CANInterface
from processor.adas_processor import ADASProcessor
from visualizer.dashboard import CLIDashboard
from processor.logger import ADASLogger
from visualizer.live_plot import LivePlot  # if you split it out
from visualizer.web_dashboard import push_data

import logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/runtime.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_live_mode(enable_plot=True):
    print("🚘 Starting live ADAS demo using vcan0...")
    logging.info("Live mode started using vcan0")

    can_interface = CANInterface()
    processor = ADASProcessor()
    dashboard = CLIDashboard()
    logger = ADASLogger()

    plotter = LivePlot() if enable_plot else None

    def update_loop():
        try:
            while True:
                sensor_data = can_interface.receive()
                if sensor_data:
                    result = processor.check_fcw(sensor_data)
                    dashboard.render(result)
                    logger.log(result)
                    if enable_plot:
                        plotter.update(result)
                    push_data(result)
        except KeyboardInterrupt:
            print("👋 Exiting live mode.")
        finally:
            can_interface.bus.shutdown()

    # Run update loop in a background thread
    thread = threading.Thread(target=update_loop, daemon=True)
    thread.start()

    # Run plotter in the main thread
    if enable_plot:
        plotter.run()
    else:
        thread.join()


def run_replay_mode(file_path, delay):
    print(f"📼 Replaying from: {file_path}")
    dashboard = CLIDashboard()
    history = []

    if not os.path.exists(file_path):
        print(f"❌ Log file not found: {file_path}")
        return

    with open(file_path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = {
                "timestamp": float(row["timestamp"]),
                "speed_kph": int(row["speed_kph"]),
                "rpm": int(row["rpm"]),
                "distance_m": float(row["distance_m"]),
                "ttc": float(row["ttc"]),
                "fcw": row["fcw"].lower() == 'true'
            }

            dashboard.render(data)
            history.append(data)
            time.sleep(delay)

    # 🔽 After replay, show the graph
    plot_replay_graph(history)


def plot_replay_graph(data_points):
    print("📊 Rendering replay graph...")
    logging.info("Rendering replay graph...")
    timestamps = [d["timestamp"] for d in data_points]
    base_time = timestamps[0]
    t = [ts - base_time for ts in timestamps]

    speed = [d["speed_kph"] for d in data_points]
    distance = [d["distance_m"] for d in data_points]
    ttc = [d["ttc"] for d in data_points]
    fcw_flags = [d["fcw"] for d in data_points]

    plt.figure(figsize=(12, 6))
    plt.title("ADAS Replay – Speed, TTC, FCW Alerts")

    plt.plot(t, speed, label="Speed (km/h)", linewidth=2)
    plt.plot(t, ttc, label="TTC (s)", linewidth=2)
    plt.plot(t, distance, label="Object Distance (m)", linestyle='--')

    alert_times = [x for x, f in zip(t, fcw_flags) if f]
    alert_ttc = [x for x, f, y in zip(fcw_flags, fcw_flags, ttc) if f]
    plt.scatter(alert_times, alert_ttc, color="red",
                label="⚠️ FCW Alert", zorder=5)

    plt.xlabel("Time (s)")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="ADAS CAN Sensor Demo")
    parser.add_argument('--mode', choices=['live', 'replay'], default='live',
                        help="Run mode: 'live' for real-time, 'replay' for playback")
    parser.add_argument('--file', type=str, default='data/demo_drive_log.csv',
                        help="CSV file for replay mode")
    parser.add_argument('--delay', type=float, default=1.0,
                        help="Delay between frames in replay mode")

    args = parser.parse_args()

    if args.mode == 'replay':
        run_replay_mode(args.file, args.delay)
    else:
        run_live_mode()


if __name__ == "__main__":
    main()
