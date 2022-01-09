import time

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

from wordle import WordleBotManager

logger = Logger(service="wordle")

# process_before_response must be True when running on FaaS
app = App(process_before_response=True)


def respond_to_slack_within_3_seconds(body, ack):
    text = body.get("text")
    if text is None or len(text) == 0:
        ack("Usage: /wordle start | /wordle guess <WORD>")
    else:
        if body["text"] is "start":
            ack(f"Welcome {body['user_name']} to Wordle!")
            bot = WordleBotManager(ctx=body)
            bot.start()


def handle_game(respond, body):
    """[options]
        ['start']
        ['guess', '<WORD>']
    """
    options = body["text"].split()

    if options[0] is "guess": # Check if we have a 'guess'
        if options[1]: # Check a word was provided
            guess = options[1]
            bot = WordleBotManager(ctx=body)
            bot.start()
            respond(bot.guess(guess=guess))
            respond(bot.letters())


@logger.inject_lambda_context
def handler(event, context: LambdaContext):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


app.command("/wordle")(
    ack=respond_to_slack_within_3_seconds,  # responsible for calling `ack()`
    lazy=[handle_game],  # unable to call `ack()` / can have multiple functions
)
