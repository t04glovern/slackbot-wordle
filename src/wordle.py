import logging
import random

from utils import WORDLEBANK, delete_wordle_game, get_wordle_game, put_wordle_game

WORDS = WORDLEBANK
WORDS_SET = set(WORDS)

logging.basicConfig(
    format="%(levelname)s - %(funcName)s() - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class WordleGame:
    def __init__(
        self,
        game_started=True,
        user=None,
        word=None,
        turns=0,
        history="",
        letters_open=list(map(chr, range(ord("A"), ord("Z") + 1))),
        letters_good=[],
    ):
        self.game_started = game_started
        self.user = user
        self.word = word
        self.turns = turns
        self.history = history
        self.letters = {
            "open": letters_open,
            "good": letters_good,
        }

    def to_json(self):
        return {
            "game_started": self.game_started,
            "user": self.user,
            "word": self.word,
            "turns": self.turns,
            "history": self.history,
            "letters": {"open": self.letters["open"], "good": self.letters["good"]},
        }

    def process_guess(self, guess):
        out_string = "`"
        letters_open = self.letters["open"]
        letters_good = self.letters["good"]

        # Make a pretty history first
        for i in range(5):
            out_string += guess[i].upper()
        out_string += "`: "

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
    def __init__(self, user_id: str):
        self.games = dict()
        item = get_wordle_game(user_id)
        if item:
            game_item = item["game"]
            if game_item:
                logger.info(
                    "WordleBot.__init__ game_item found for {} with value: {}".format(
                        user_id, game_item
                    )
                )
                game = WordleGame(
                    game_started=game_item["game_started"],
                    user=game_item["user"],
                    word=game_item["word"],
                    turns=game_item["turns"],
                    history=game_item["history"],
                    letters_open=game_item["letters"]["open"],
                    letters_good=game_item["letters"]["good"],
                )
                self.games[user_id] = game
            else:
                logger.info(
                    "WordleBot.__init__ game_item NOT found for {}".format(user_id)
                )
        else:
            logger.info("WordleBot.__init__ game_item NOT found for {}".format(user_id))

    def checkGame(self, user_id: str):
        logger.info("checkGame for {}".format(user_id))
        return user_id in self.games

    def deleteGame(self, user_id: str):
        logger.info("deleteGame for {}".format(user_id))
        if self.checkGame(user_id):
            delete_wordle_game(user_id)
            del self.games[user_id]
            return 0
        return 1

    def addGame(self, user_id: str, game: WordleGame):
        logger.info("addGame for {}".format(user_id))
        if self.checkGame(user_id):
            logger.info("addGame game already exists for {}".format(user_id))
            return False
        else:
            logger.info("addGame game didn't exists for {}. Adding one".format(user_id))
            self.games[user_id] = game

    def saveGame(self, user_id: str):
        logger.info("saveGame for {}".format(user_id))
        game = self.getGame(user_id)
        if game:
            put_wordle_game(user_id=user_id, game=game)
            return 1
        return 0

    def getGame(self, user_id: str):
        logger.info("getGame for {}".format(user_id))
        if self.checkGame(user_id):
            return self.games[user_id]
        else:
            logger.info("getGame: None found")
            return None


class WordleBotManager:
    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = WordleBot(ctx["user_id"])

    def start(self):
        """Starts a new Wordle game if one hasn't begun already."""
        uid = self.ctx["user_id"]

        if self.bot.checkGame(uid):
            logger.info(
                "[RESPOND]: "
                + "Game already started. End the game first before starting a new one."
            )
            return

        logger.info("[RESPOND]: " + "Starting standard game of Wordle...")
        word = random.choice(WORDS)

        user = self.ctx["user_id"]
        self.bot.addGame(uid, WordleGame(user=user, word=word))
        self.bot.saveGame(uid)

    def review(self):
        """Review your previous guesses."""
        logger.info("[RESPOND]: " + "Your guesses so far are:")
        game = self.bot.getGame(self.ctx["user_id"])
        logger.info("[SEND]: " + game.getHistory())
        # CUSTOM RETURN
        return game.getHistory()

    def letters(self):
        """Get which letters are still possible."""
        game = self.bot.getGame(self.ctx["user_id"])
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

    def guess(self, guess):
        """Make a guess in a wordle game."""
        guess = guess.upper()
        uid = self.ctx["user_id"]
        print(f"Attempted guess by [{uid}] was {guess}")
        if len(guess) != 5:
            logger.info("[RESPOND]: " + "Guess invalid, needs to be 5 letters.")
            return
        if guess not in WORDS_SET:
            logger.info(
                "[RESPOND]: " + "Guess invalid, needs to be real 5 letter word."
            )
            return
        logger.info("[RESPOND]: " + f"Your guess was: {guess}")
        game = self.bot.getGame(uid)
        guess_result, response = game.process_guess(guess)
        logger.info("[SEND]: " + game.getHistory())
        logger.info("[SEND]: " + response)
        if guess_result == -1 or guess_result == 1:
            # Game over
            self.bot.deleteGame(uid)
        else:
            # Save game
            self.bot.saveGame(uid)
        # CUSTOM RETURN
        return game.getHistory() + "\n" + response

    def end(self):
        """Ends game in current guild."""
        uid = self.ctx["user_id"]
        game = self.bot.getGame(uid)
        word = game.endGame()
        logger.info("[RESPOND]: " + f"Game over! The word was {word}")
        self.bot.deleteGame(uid)
