from flask import Flask, render_template, request
import requests
import time
import json

app = Flask(__name__)
PP_ADDRESS = "http://192.168.86.38/"
PP_CHANNELS = ['accX', 'accY', 'accZ']
run = False  # Declare as a global variable

@app.route('/')
def index():
    # Pass 'message' as None initially
    return render_template('index.html', message=None)

@app.route('/data_retrieve', methods=['POST'])
def data_retrieve():
    global run  # Access the global 'run' variable
    run = True
    # Simulate running a method
    message = "Method has been triggered!"
    
    while run:
        print("METHOD IS TRIGGERING !!!")
        time.sleep(1)  # Sleep to avoid locking the CPU with an infinite loop
        # Uncomment and modify this block when you're ready to fetch data from Phyphox
        # url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
        # try:
        #     getRequest = requests.get(url).text
        # except:
        #     print("No Data At the Moment, Please Restart")
        #     break
        # data = json.loads(getRequest)
        # for channel in PP_CHANNELS:
        #     acc_data = data['buffer'][channel]['buffer'][0]
        #     print(f'{acc_data:10.7}', end='\t')

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
