from helper import send_message
from helper import text_resources
from flask import Flask, request

app = Flask(__name__)

# Define route for home page
@app.route('/')
def home():
    return 'Processing successfully'

# Define route for receiving messages from Twilio
@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        # Extract incoming parameters from Twilio
        message = request.form['Body']
        sender_id = request.form['From']

        # Get response from OpenAI
        result = text_resources(message)

        # Send response back to sender via Twilio
        if result['status'] == 1:
            send_message(sender_id, result['response'])
    except:
        pass

    # Return OK status code
    return 'OK', 200