from flask import Flask, render_template, request
import requests
import time
import json
import os
from datetime import datetime

app = Flask(__name__)
PP_ADDRESS = "http://192.168.86.38/"
PP_CHANNELS = ['accX', 'accY', 'accZ']
run = False  # Declare as a global variable

# Directory to save data files
DATA_DIR = 'data_files'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def index():
    # Pass 'message' as None initially
    return render_template('index.html', message=None)

@app.route('/data_retrieve', methods=['POST'])
def data_retrieve():
    global run  # Access the global 'run' variable
    run = True
    # Generate a unique filename with a timestamp
    filename = os.path.join(DATA_DIR, f'data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')

    # Open the file in write mode
    with open(filename, 'w') as f:
        message = "Method has been triggered!"
        
        while run:
            time.sleep(0.1)  # Sleep to avoid locking the CPU with an infinite loop
            url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
            try:
                getRequest = requests.get(url).text
            except:
                print("No Data At the Moment, Please Restart")
                break
            
            data = json.loads(getRequest)
            
            # Write the data to the file
            for channel in PP_CHANNELS:
                acc_data = data['buffer'][channel]['buffer'][0]
                print(f'{channel}: {acc_data:10.7}\n')
                f.write(f'{channel}: {acc_data:10.7}\n')
            
            f.write('\n')  # Add a newline after each data point for clarity

            # Check for `run` being False to stop the loop
            if not run:
                break

    return render_template('index.html', message=message)

@app.route('/end_data', methods=['POST'])
def data_stop():
    global run  # Access the global 'run' variable
    run = False  # Stop the data collection loop
    return render_template('index.html', message='STOPPED METHOD')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
