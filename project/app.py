import time
import requests
import numpy as np
import json
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Replace this with your Phyphox device's IP address and port
phyphox_url = 'http://192.168.86.38:80/get?format=json'

# Initialize the Dash app
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Initialize data storage
time_values = []
acc_magnitude_values = []
sleep_stages = []

# File path for storing data
data_file = 'data.json'

# Dash layout
dash_app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
    html.Div(id='sleep-summary', style={'padding': '20px', 'font-size': '20px'})
])

# Fetch data from Phyphox
def fetch_phyphox_data():
    try:
        response = requests.get(phyphox_url)
        data = response.json()
        
        # Assuming you are using acceleration data
        accX = data['buffer']['accX']['buffer'][-1]
        accY = data['buffer']['accY']['buffer'][-1]
        accZ = data['buffer']['accZ']['buffer'][-1]
        
        return accX, accY, accZ
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Phyphox data: {e}")
        return None, None, None

# Determine sleep stage based on acceleration magnitude
def detect_sleep_stage(magnitude):
    if magnitude is None:
        return 'No Data'
    if magnitude < 0.1:
        return 'Deep Sleep'
    elif magnitude < 0.3:
        return 'Light Sleep'
    else:
        return 'Awake'

# Save data to a file
def save_data():
    with open(data_file, 'w') as file:
        json.dump({
            'time_values': time_values,
            'acc_magnitude_values': acc_magnitude_values,
            'sleep_stages': sleep_stages
        }, file)

# Update the graph
@dash_app.callback(
    Output('live-graph', 'figure'),
    Output('sleep-summary', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n_intervals):
    # Fetch data from Phyphox
    accX, accY, accZ = fetch_phyphox_data()
    if accX is None or accY is None or accZ is None:
        return {'data': [], 'layout': go.Layout(title='No data')}, 'Error: Could not fetch data'

    acc_magnitude = np.sqrt(accX**2 + accY**2 + accZ**2)
    
    # Update time and data values
    now = time.strftime('%H:%M:%S', time.localtime())
    time_values.append(now)
    acc_magnitude_values.append(acc_magnitude)

    # Detect sleep stage
    sleep_stage = detect_sleep_stage(acc_magnitude)
    sleep_stages.append(sleep_stage)

    # Save data to file
    save_data()

    # Plot the acceleration magnitude over time
    figure = {
        'data': [
            go.Scatter(x=time_values, y=acc_magnitude_values, mode='lines', name='Acceleration Magnitude')
        ],
        'layout': go.Layout(
            title='Live Sleep Data',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Acceleration Magnitude', range=[0, 1]),
            margin=dict(l=40, r=0, t=40, b=30),
            autosize=True,
        )
    }

    # Build a summary of the sleep stages
    summary_html = []
    for i, stage in enumerate(sleep_stages):
        summary_html.append(f'{time_values[i]}: {stage}<br>')

    return figure, ''.join(summary_html)

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    socketio.emit('status_update', {'status': 'started'})
    return jsonify({'status': 'started'})

@app.route('/stop')
def stop():
    socketio.emit('status_update', {'status': 'stopped'})
    return jsonify({'status': 'stopped'})

@app.route('/analyze')
def analyze():
    analysis_results = [{'time': time_values[i], 'sleep_period': sleep_stages[i]} for i in range(len(time_values))]
    return jsonify(analysis_results)

@app.route('/data')
def get_data():
    try:
        with open(data_file, 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'No data available'}), 404

# Run the Flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)
