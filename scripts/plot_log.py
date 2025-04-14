import csv
import matplotlib.pyplot as plt
import os


def plot_csv(file_path="data/demo_drive_log.csv"):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    timestamps, speed, distance, ttc, fcw = [], [], [], [], []

    with open(file_path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(float(row["timestamp"]))
            speed.append(int(row["speed_kph"]))
            distance.append(float(row["distance_m"]))
            ttc.append(float(row["ttc"]))
            fcw.append(row["fcw"].lower() == "true")

    # Normalize timestamps to seconds from start
    base_time = timestamps[0]
    timestamps = [t - base_time for t in timestamps]

    # Plot
    plt.figure(figsize=(12, 6))
    plt.title("ADAS Drive Log – Speed, TTC, and FCW Alerts")

    plt.plot(timestamps, speed, label="Speed (km/h)", linewidth=2)
    plt.plot(timestamps, ttc, label="TTC (s)", linewidth=2)
    plt.plot(timestamps, distance, label="Object Distance (m)", linestyle="--")

    # Highlight FCW alerts
    alert_times = [t for t, f in zip(timestamps, fcw) if f]
    alert_ttc = [t for t, f in zip(ttc, fcw) if f]
    plt.scatter(alert_times, alert_ttc, color="red",
                label="⚠️ FCW Triggered", zorder=5)

    plt.xlabel("Time (s)")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_csv()
