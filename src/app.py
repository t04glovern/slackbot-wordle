import time

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)


def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        ack("Usage: /start-process (description here)")
    else:
        ack(f"Accepted! (task: {body['text']})")


def run_long_process(respond, body):
    time.sleep(5)  # longer than 3 seconds
    respond(f"Completed! (task: {body['text']})")


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


app.command("/start-process")(
    ack=respond_to_slack_within_3_seconds,  # responsible for calling `ack()`
    lazy=[run_long_process],  # unable to call `ack()` / can have multiple functions
)
