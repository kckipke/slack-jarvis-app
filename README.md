This is an interactive bot for Slack, named Jarvis after Tony Stark's virtual assistant in Iron Man. This bot doesn't really do anythign functional; I made it as a joke for my friends and
our Slack workspace (because "Jarvis enhance" is just such a quotable line whenever you see an interesting image). I also wanted to gain experience with the Slack API because
I would like to make a Slack to Google Photos tool soon. I did learn a lot, and incorporated a variety of Slack features.

Jarvis will:
- Ask users if they want to enhance an image, presenting a button. If clicked, Jarvis will send back a cropped ("zoomed in") version of the photo.
- Respond to his name being said in a channel and will offer users three options in a reply: timepicker, user select, or button:
  - The timepicker is to schedule "hero time" and once picked, Jarvis will announce to the channel when that user will be heroic.
  - The user select is to nominate "Hero of the Week." Once nominated, Jarvis will ask user for rationale with a text box, and will then send the
    nomination and rationale in the main channel.
  - The button, if clicked, is for Jarvis to send a random super hero photo.

In order to use this in your workspace, you will need to set up a Slack developer account, create a Slack app, and then export your SLACK_BOT_TOKEN and SLACK_APP_TOKEN
as environment variables (you can also add them to the setup_vars script to be a bit easier/quicker).
