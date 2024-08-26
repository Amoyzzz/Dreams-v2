from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    # Pass 'message' as None initially
    return render_template('index.html', message=None)

@app.route('/data_retrieve', methods=['POST'])
def data_retrieve():
    # Run your method here (for now just adding a message)
    message = "Method has been triggered!"
    
    # Render the template again, passing the message to the front-end
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
