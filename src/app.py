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
    """[options]
        ['start']
        ['guess', '<WORD>']
    """
    text = body.get("text")
    options = text.split()
    logger.info("respond_to_slack_within_3_seconds request options: {}".format(options))
    if options is None or len(options) == 0:
        ack("Usage: /wordle start | /wordle guess <WORD>")
    else:
        if options[0] == "start":
            bot = WordleBotManager(ctx=body)
            bot.start()
            ack(f"Welcome {body['user_name']} to Wordle!, use /wordle guess <WORD>\n{bot.review()}\n{bot.letters()}")
        elif options[0] == "guess": # Check if we have a 'guess'
            if options[1]: # Check a word was provided
                guess = options[1]
                bot = WordleBotManager(ctx=body)
                bot.start()
                ack(bot.guess(guess=guess))


def handle_game(respond, body):
    """[options]
        ['start']
        ['guess', '<WORD>']
    """
    text = body.get("text")
    options = text.split()
    logger.info("handle_game request options: {}".format(options))

    # if options[0] == "guess": # Check if we have a 'guess'
    #     if options[1]: # Check a word was provided
    #         guess = options[1]
    #         bot = WordleBotManager(ctx=body)
    #         bot.start()
    #         respond(bot.guess(guess=guess))
    #         respond(bot.letters())


@logger.inject_lambda_context
def handler(event, context: LambdaContext):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


app.command("/wordle")(
    ack=respond_to_slack_within_3_seconds,  # responsible for calling `ack()`
    lazy=[handle_game],  # unable to call `ack()` / can have multiple functions
)
