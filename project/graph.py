import os
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

data_file = 'sleep_data.txt'

def read_data_from_file():
    time_values = []
    acc_magnitude_values = []
    sleep_stages = []

    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                time, magnitude, stage = line.strip().split(', ')
                time_values.append(time)
                acc_magnitude_values.append(float(magnitude))
                sleep_stages.append(stage)

    return time_values, acc_magnitude_values, sleep_stages

def create_graph_layout(dash_app):
    dash_app.layout = html.Div([
        dcc.Graph(id='live-graph'),
        dcc.Interval(id='interval-component', interval=250, n_intervals=0),  # Update every 0.25 seconds
        html.Div(id='sleep-summary', style={'padding': '20px', 'font-size': '20px'})
    ])

    @dash_app.callback(
        Output('live-graph', 'figure'),
        Output('sleep-summary', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph(n_intervals):
        time_values, acc_magnitude_values, sleep_stages = read_data_from_file()

        if not time_values:
            return {'data': [], 'layout': go.Layout(title='No data')}, 'No data available'

        # Filter data to only include the last 100 seconds
        cutoff_time = (datetime.now() - timedelta(seconds=100)).strftime('%H:%M:%S')
        filtered_time_values = [t for t in time_values if t >= cutoff_time]
        filtered_acc_magnitude_values = acc_magnitude_values[-len(filtered_time_values):]
        filtered_sleep_stages = sleep_stages[-len(filtered_time_values):]

        figure = {
            'data': [
                go.Scatter(x=filtered_time_values, y=filtered_acc_magnitude_values, mode='lines', name='Acceleration Magnitude')
            ],
            'layout': go.Layout(
                title='Live Sleep Data',
                xaxis=dict(title='Time', type='date', range=[filtered_time_values[0], filtered_time_values[-1]]),
                yaxis=dict(title='Acceleration Magnitude', range=[0, 1]),
                autosize=True
            )
        }

        summary_html = [f'{time}: {stage}<br>' for time, stage in zip(filtered_time_values, filtered_sleep_stages)]
        
        return figure, ''.join(summary_html)
