import os
import logging
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


# Shared buffer to receive updates from ADAS processor
data_buffer = []

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "dash.log")

log = logging.getLogger('werkzeug')  # Flask + Dash logger
log.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
log.addHandler(file_handler)


def push_data(data_point):
    data_buffer.append(data_point)
    if len(data_buffer) > 100:
        data_buffer.pop(0)


# Dash app setup
app = dash.Dash(__name__)
app.title = "ADAS Web Dashboard"

app.layout = html.Div([
    html.H1("ADAS Real-Time Visualizer"),
    dcc.Graph(id='graph'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])


@app.callback(
    Output('graph', 'figure'),
    Input('interval', 'n_intervals')
)
def update_graph(n):
    try:
        if not data_buffer:
            return {"data": [], "layout": {"title": "Waiting for data..."}}

        t = [d["timestamp"] - data_buffer[0]["timestamp"] for d in data_buffer]
        speed = [d["speed_kph"] for d in data_buffer]
        ttc = [d["ttc"] for d in data_buffer]
        distance = [d["distance_m"] for d in data_buffer]
        fcw = [d["fcw"] for d in data_buffer]

        return {
            "data": [
                {"x": t, "y": speed, "type": "line", "name": "Speed (km/h)"},
                {"x": t, "y": ttc, "type": "line", "name": "TTC (s)"},
                {"x": t, "y": distance, "type": "line",
                    "name": "Distance (m)"},
                {"x": [x for x, f in zip(t, fcw) if f],
                 "y": [y for y, f in zip(ttc, fcw) if f],
                 "type": "scatter", "mode": "markers", "name": "⚠️ FCW", "marker": {"color": "red", "size": 10}},
            ],
            "layout": {
                "title": "ADAS Live Data",
                "xaxis": {"title": "Time (s)"},
                "yaxis": {"title": "Values"},
            }
        }

    except Exception as e:
        print(f"❌ Dash graph update error: {e}")
        logging.info(f"❌ Dash graph update error: {e}")
        return {"data": [], "layout": {"title": "Error occurred"}}


def run_dashboard():
    print("🚀 Dash server is starting...")
    logging.info("Dash server is starting...")
    # app.run_server(debug=False, use_reloader=False)
    app.run(debug=True)
