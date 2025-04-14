import os
import time


class CLIDashboard:
    def __init__(self):
        pass

    def clear_screen(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception:
            print("\n" * 5)

    def render(self, data):
        try:
            self.clear_screen()
            print("=== 🚘 ADAS CAN Dashboard ===")
            print(f"Time        : {time.strftime('%H:%M:%S')}")
            print(f"Speed       : {data.get('speed_kph', 'N/A')} km/h")
            print(f"RPM         : {data.get('rpm', 'N/A')}")
            print(f"Distance    : {data.get('distance_m', 0.0):.2f} m")
            print(f"TTC         : {data.get('ttc', 0.0):.2f} s")
            print(f"FCW Trigger : {'⚠️ YES' if data.get('fcw') else '✔️ NO'}")
            print("=" * 30)
        except Exception as e:
            print(f"❌ Dashboard render error: {e}")
