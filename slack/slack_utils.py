import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOEKN')

client = WebClient(token=SLACK_BOT_TOKEN)

def send_dm(user_id, message):
    """Send a direct message (DM) to a Slack user."""
    try:
        response = client.chat_postMessage(channel=user_id, text=message)
        print(f"DM sent successfully: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Error sending DM: {e.response['error']}")

def send_channel_message(channel_id, message):
    """Send a message to a Slack channel."""
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        print(f"Message sent successfully to channel: {response['channel']}")
    except SlackApiError as e:
        print(f"Error sending message to channel: {e.response['error']}")

def upload_file_to_channel(channel_id, file_path, title):
    """Upload a file to a Slack channel."""
    try:
        response = client.files_upload_v2(channels=[channel_id], file=file_path, title=title)
        print(f"File uploaded successfully: {response['file']['id']}")
    except SlackApiError as e:
        print(f"Error uploading file: {e.response['error']}")
