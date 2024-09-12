import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from PIL import Image
import tempfile
import requests
import io
import random

CHANNEL_ID_CONST =  'C0760L165N1'
DEFAULT_FILE_CONST = "the-avengers.jpg"

# Initializes app with bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Default file path if later file download fails
shared_file = {
    "filename": "IMG_5862.jpeg",
    "channel_id": CHANNEL_ID_CONST,
}

@app.event("file_shared")
def file_share(event, say, ack):
    """Detect when files are shared in relevant channel."""
    ack()
    if event['channel_id'] == CHANNEL_ID_CONST:
        # Get sent file info
        image_id = event['file_id']
        downloadable_file = app.client.files_info(file=image_id).data['file']['url_private_download']

        # Overwrite shared file
        shared_file['filename'] = downloadable_file
        shared_file['channel_id'] = event['channel_id']

        # Send response message into channel
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Hey there <@{event['user_id']}>! I see you've sent an image! Would you like to enhance?"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Enhance"},
                        "action_id": "button_click"
                    }
                }
            ],
            text=f"Hey there <@{event['user_id']}>! I see you've sent an image! Unfortunately, I can't enhance right now."
        )


@app.message("Jarvis")
def message_hello(message, say, ack):
    """Listens for incoming messages that contain 'Jarvis'."""

    ack()
    if message['channel'] == CHANNEL_ID_CONST:
        thread = message['ts']
        # Send response message
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>! I'm Jarvis, your personal assistant! What would you like to do?"}
                },
                {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Schedule world saving time"
                        },
                        "style": "primary",
                        "action_id": "schedule_world_saving_time"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Nominate an Avenger for Hero of the Week"
                        },
                        "style": "primary",
                        "action_id": "nominate"
                    },
                                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "See a heroic photo"
                        },
                        "style": "primary",
                        "action_id": "photo"
                    }
                ]
                }
            ],
            text=f"Hey there <@{message['user']}>! I'm Jarvis, your personal assistant!",
            thread_ts=thread
        )

@app.action("photo")
def present_photo(body, ack, say):
    """Sends a random superhero photo."""
    ack()
    urls = [
        "https://www.pluggedin.com/wp-content/uploads/2019/12/the-avengers-review-image-1200x688.jpg",
        "https://cdn.mos.cms.futurecdn.net/xGwDeehYUPAaTZqSeuHUv8.jpg",
        "https://static1.srcdn.com/wordpress/wp-content/uploads/2024/02/aaa-mcu-multiverse-saga-characters-1-pxlr.jpg",
        "https://images.immediate.co.uk/production/volatile/sites/3/2023/06/Marvel-Movies-In-Order-Avengers-Endgame-ef06bfd.jpg?quality=90&resize=620,414",
        "https://cdn.marvel.com/content/1x/002irm_ons_mas_mob_01_0.jpg",
        "https://decider.com/wp-content/uploads/2024/04/Captain-America-The-Winter-Soldier-THROWBACK.jpg?quality=75&strip=all&w=1200"
        ]
    photo_link = random.choice(urls)
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{body['user']['id']}>! asked for a heroic photo! Here you go!:"}
            },
            {
                "type": "image",
                "image_url": photo_link,
                "alt_text": "heroic photo"
            }
        ],
        text=f"<@{body['user']['id']}>! asked for a heroic photo! Here you go!:"
    )

@app.action("nominate")
def nominate(body, ack, say):
    """Sends in channel which user was nominated for Hero of the Week."""
    ack()
    say(
        blocks = [
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select Hero"
                    },
                    "action_id": "hero_entered",
                    "max_selected_items": 1
                },
                "label": {
                    "type": "plain_text",
                    "text": "Nominate for Hero of the Week!"
                }
            }
        ],
        text="Let us know who you nominate!",
        thread_ts=body['container']['thread_ts']
    )

@app.action("hero_entered")
def ask_why(body, ack, say):
    """Ask for rationale behind Hero of the Week."""
    ack()
    say( 
        blocks = [
            {
            "dispatch_action": True,
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "rationale_provided"
            },
            "label": {
                "type": "plain_text",
                "text": "Please explain why they deserve Hero of the Week",
            }
            }
        ],
        text=body['actions'][0]['selected_users'][0],
        thread_ts=body['container']['thread_ts']
    )

@app.action("schedule_world_saving_time")
def schedule(body, ack, say):
    """Display time picker."""
    ack()
    say(
        blocks = [
            {
			"type": "section",
			"block_id": "section1234",
			"text": {
				"type": "mrkdwn",
				"text": "Select a time to get freaky."
			},
			"accessory": {
				"type": "timepicker",
				"timezone": "America/Detroit",
				"action_id": "timepicker123",
				"initial_time": "11:50",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a time to save the world"
				}
			}
		}
        ],
        text="Pick a time",
        thread_ts=body['container']['thread_ts']
    )

@app.action("rationale_provided")
def thank_you(body, ack, say):
    """Send thank you message for nomination."""
    ack()
    say(f"Thank you <@{body['user']['id']}> for your nomination of <@{body['message']['text']}> for Hero of the Week! Here's why you think they deserve it: \"{body['actions'][0]['value']}\" \n<!channel> what do we think?")


@app.action("timepicker123")
def set_reminder(body, ack, say):
    """Announces time selection."""
    ack()
    say(f"Great! <!channel>, let it be known that <@{body['user']['id']}> will be saving the world at {body['state']['values']['section1234']['timepicker123']['selected_time']} EST")

@app.action("button_click")
def action_button_click(body, ack, say):
    """Crops and sends image when user presses Enhance button."""
    ack()

    say("Enhancing...")

    success = False
    if shared_file['filename'] == "CHANNEL_ID_CONST":
        image_content = open('CHANNEL_ID_CONST', 'rb')
        image_content = image_content.read()
        image_content = bytearray(image_content)
        say('Uh oh! Image enhance failed. Enjoy this default heroic image instead:')
    else:
        #   Download the file from the internet
        image_content = requests.get(
            url=shared_file['filename'], 
            headers={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
        ).content
        success = True

    # Open the image content in PIL
    with Image.open(io.BytesIO(image_content)) as img:
        # Crop the image
        width, height = img.size
        left = width - (0.65 * width)
        top = height - (0.65 * height)
        right = width - (0.35 * width)
        bottom = height - (0.35 * height)
        if success:
            img_cropped = img.crop((left, top, right, bottom))
        else:
            img_cropped = img

        # Save the cropped image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_img:
            try:
                img_cropped.save(tmp_img)
                tmp_img.flush()
                tmp_img.seek(0)
                say(f"Here's your enhanced image, <@{body['user']['id']}>! Enjoy!")
            except: 
                say("I can't enhance that file format! Try with a different image--or not using a ss! For now, enjoy this default pic: ")
                tmp_img = open('CHANNEL_ID_CONST', 'rb')

            # Upload URL and file ID from Slack API
            slack_upload = app.client.files_getUploadURLExternal(
                filename=tmp_img.name, 
                length=os.path.getsize(tmp_img.name)
            )
            upload_url = slack_upload['upload_url']
            file_id = slack_upload['file_id']
            slack_key = os.environ.get("SLACK_BOT_TOKEN")

            # Prepare the headers and file payload for the upload
            headers = {
                'Authorization': f'Bearer {slack_key}',
            }
            files = {
                'file': (os.path.basename(tmp_img.name), open(tmp_img.name, 'rb')),
            }

            # Perform the file upload via the URL provided by Slack
            response = requests.post(upload_url, headers=headers, files=files)

            # Check for success
            if response.status_code == 200:
                print("File uploaded successfully!")
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
                print(response.text)

            # Complete the upload process with Slack
            app.client.files_completeUploadExternal(
                files=[{"id": str(file_id), "title": "freaky"}], 
                channel_id=shared_file['channel_id']
            )
            ack()

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()