import logging
import random

from utils import WORDLEBANK

WORDS = WORDLEBANK
WORDS_SET = set(WORDS)

logging.basicConfig(
    format="%(levelname)s - %(funcName)s() - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class WordleGame:
    def __init__(self, user, word):
        self.game_started = True
        self.user = user
        self.word = word
        self.turns = 0
        self.history = ""
        self.letters = {
            "open": list(map(chr, range(ord("A"), ord("Z") + 1))),
            "good": [],
        }
        print(f"Game started by {user} with word {word}.")

    def process_guess(self, guess):
        out_string = ""
        letters_open = self.letters["open"]
        letters_good = self.letters["good"]

        # Make a pretty history first
        for i in range(5):
            out_string += f":regional_indicator_{guess[i].lower()}: "
        out_string += "\n"

        for i in range(5):
            if guess[i] in letters_open:
                letters_open.remove(guess[i])

            if guess[i] == self.word[i]:
                out_string += ":large_green_square: "
                if guess[i] not in letters_good:
                    letters_good.append(guess[i])
            elif guess[i] in self.word:
                out_string += ":large_yellow_square: "
                if guess[i] not in letters_good:
                    letters_good.append(guess[i])
            else:
                out_string += ":black_large_square: "
        out_string += "\n"
        self.history += out_string
        self.turns += 1
        if guess == self.word:
            return (1, f"You won in {self.turns} turns!")  # win
        if self.turns == 6:
            return (-1, f"You lost! The word was {self.word}.")  # loss
        return (
            0,
            f"You still have {6-self.turns} "
            + ("turn" if self.turns == 5 else "turns")
            + " left!",
        )

    def endGame(self):
        self.turns = 6
        return self.word

    def getHistory(self):
        if self.history == "":
            return "No guesses."
        return self.history

    def getLetters(self):
        return self.letters


class WordleBot:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.games = dict()

    def on_command_error(self, ctx, error):
        logger.info(f"Error: {error}")

    ## Custom functions
    def checkGame(self, user_id: int):
        return user_id in self.games

    def deleteGame(self, user_id: int):
        if self.checkGame(user_id):
            del self.games[user_id]
            return 0
        return 1

    def addGame(self, user_id: int, game: WordleGame):
        if self.checkGame(user_id):
            return False
        else:
            self.games[user_id] = game

    def getGame(self, user_id: int):
        if self.checkGame(user_id):
            return self.games[user_id]
        else:
            return None


bot = WordleBot()


def start(ctx):
    """Starts a new Wordle game if one hasn't begun already."""
    uid = ctx["user_id"]

    if bot.checkGame(uid):
        logger.info(
            "[RESPOND]: "
            + "Game already started. End the game first before starting a new one."
        )
        return

    logger.info("[RESPOND]: " + "Starting standard game of Wordle...")
    word = random.choice(WORDS)

    user = ctx["user_id"]
    bot.addGame(uid, WordleGame(user, word))


def review(ctx):
    """Review your previous guesses."""
    logger.info("[RESPOND]: " + "Your guesses so far are:")
    game = bot.getGame(ctx["user_id"])
    logger.info("[SEND]: " + game.getHistory())
    # CUSTOM RETURN
    return game.getHistory()


def letters(ctx):
    """Get which letters are still possible."""
    game = bot.getGame(ctx["user_id"])
    logger.info("[RESPOND]: " + "Your available letters are:")
    for k, v in game.getLetters().items():
        if k == "open":
            logger.info("[SEND]: " + f":white_circle: Open letters: {' '.join(v)}")
            # CUSTOM RETURN
            return f":white_circle: Open letters: {' '.join(v)}"
        else:
            logger.info("[SEND]: " + f":green_circle: Found letters: {' '.join(v)}")
            # CUSTOM RETURN
            return f":green_circle: Found letters: {' '.join(v)}"


def guess(ctx, guess):
    """Make a guess in a wordle game."""
    guess = guess.upper()
    uid = ctx["user_id"]
    print(f"Attempted guess by [{uid}] was {guess}")
    if len(guess) != 5:
        logger.info("[RESPOND]: " + "Guess invalid, needs to be 5 letters.")
        return
    if guess not in WORDS_SET:
        logger.info("[RESPOND]: " + "Guess invalid, needs to be real 5 letter word.")
        return
    logger.info("[RESPOND]: " + f"Your guess was: {guess}")
    game = bot.getGame(uid)
    guess_result, response = game.process_guess(guess)
    logger.info("[SEND]: " + game.getHistory())
    logger.info("[SEND]: " + response)
    if guess_result == -1 or guess_result == 1:
        # Game over
        bot.deleteGame(uid)
    # CUSTOM RETURN
    return game.getHistory() + "\n" + response


def end(ctx):
    """Ends game in current guild."""
    uid = ctx["user_id"]
    game = bot.getGame(uid)
    word = game.endGame()
    logger.info("[RESPOND]: " + f"Game over! The word was {word}")
    bot.deleteGame(uid)
