import os
import openai
from twilio.rest import Client
from dotenv import load_dotenv
from flask import Flask, request

# Load environment variables from.env file
load_dotenv()

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Set Twilio account SID and auth token
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Define function to send message via Twilio
def send_message(to: str, message: str) -> None:
    _ = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=to
    )

# Define function to get response from OpenAI
def text_resources(prompt: str) -> dict:
    try:
        # Create OpenAI object
        llm = OpenAI()

        # Send prompt to OpenAI and get response
        response = llm.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt},
            ]
        )

        # Return response as dictionary
        return {
            'status': 1,
            'response': response.choices[0].message.content
        }
    except:
        # Return error message if request to OpenAI fails
        return {
            'status': 0,
            'response': ''
        }

# Create Flask web application
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

# Start Flask web application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


