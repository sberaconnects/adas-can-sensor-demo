import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque


class LivePlot:
    def __init__(self, max_len=30):
        self.max_len = max_len
        self.t = deque(maxlen=max_len)
        self.speed = deque(maxlen=max_len)
        self.ttc = deque(maxlen=max_len)
        self.fcw = deque(maxlen=max_len)

        self.start_time = None
        self.fig, self.ax = plt.subplots()
        self.lines = {
            "speed": self.ax.plot([], [], label="Speed (km/h)", color='blue')[0],
            "ttc": self.ax.plot([], [], label="TTC (s)", color='orange')[0],
            "alerts": self.ax.plot([], [], 'ro', label="FCW Alert")[0],
        }

        self.ax.set_xlim(0, self.max_len)
        self.ax.set_ylim(0, 150)
        self.ax.legend()
        self.ax.set_title("ADAS Live Plot")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Values")

    def update(self, data_point):
        ts = data_point["timestamp"]
        if self.start_time is None:
            self.start_time = ts
        elapsed = ts - self.start_time

        self.t.append(elapsed)
        self.speed.append(data_point["speed_kph"])
        self.ttc.append(data_point["ttc"])
        self.fcw.append(data_point["fcw"])

    def animate(self, frame):
        self.lines["speed"].set_data(self.t, self.speed)
        self.lines["ttc"].set_data(self.t, self.ttc)
        alert_x = [t for t, f in zip(self.t, self.fcw) if f]
        alert_y = [t for t, f in zip(self.ttc, self.fcw) if f]
        self.lines["alerts"].set_data(alert_x, alert_y)

        self.ax.set_xlim(
            max(0, self.t[0] if self.t else 0), self.t[-1] + 1 if self.t else self.max_len)
        return self.lines.values()

    def run(self):
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=1000, cache_frame_data=False
        )
        plt.show()
