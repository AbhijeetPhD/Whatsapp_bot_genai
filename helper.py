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