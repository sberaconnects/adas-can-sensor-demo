# scripts/run_live_web.py

from visualizer.web_dashboard import run_dashboard
from main import run_live_mode
import threading

if __name__ == "__main__":
    threading.Thread(target=run_live_mode, kwargs={
                     'enable_plot': False}, daemon=True).start()
    run_dashboard()
