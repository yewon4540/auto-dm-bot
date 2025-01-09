import os
import pymysql
import time
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

# Slack Bot Token (OAuth Token)
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOEKN')
YEWON = os.getenv('YEWON')
CHANNEL = os.getenv('CHANNEL')

print("변수 확인 시작")
print(SLACK_BOT_TOKEN)
print(YEWON)
print(CHANNEL)
print("변수 확인 끝")

def send_dm(user_id, message):
    """Send a direct message (DM) to a Slack user."""
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        response = client.chat_postMessage(
            channel=user_id,  # User ID to send the DM
            text=message
        )
        print(f"DM sent successfully: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Error sending DM: {e.response['error']}")

def send_channel_message(channel_id, message):
    """Send a message to a Slack channel."""
    client = WebClient(token=SLACK_BOT_TOKEN)
    try:
        response = client.chat_postMessage(
            channel=channel_id,  # Channel ID to send the message
            text=message
        )
        print(f"Message sent successfully to channel: {response['channel']}")
    except SlackApiError as e:
        print(f"Error sending message to channel: {e.response['error']}")

if __name__ == "__main__":
    while True:
        print("Select an option:")
        print("1: Send a DM to a user")
        print("2: Send a message to a channel")
        print("Other: Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # user_id = input("Enter the Slack User ID: ")
            user_id = YEWON
            dm_message = input("Enter the message to send: ")
            send_dm(user_id, dm_message)
        elif choice == "2":
            # channel_id = input("Enter the Slack Channel ID: ")
            channel_id = CHANNEL
            channel_message = input("Enter the message to send: ")
            send_channel_message(channel_id, channel_message)
        else:
            print("Exiting...")
            break

