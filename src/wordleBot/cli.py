#!/usr/bin/env python3

# Solver for wordle: https://www.nytimes.com/games/wordle/index.html
# Copyright Illumihax, 9qUmV4

import argparse
import logging
import re
import sys

from .wordleSolver import WordleSolver

# Logging
LOG_LEVEL = {
    "CRITICAL": logging.CRITICAL, 
    "ERROR": logging.ERROR, 
    "WARNING": logging.WARNING, 
    "INFO": logging.INFO, 
    "DEBUG": logging.DEBUG
}


class WordleBotCLI():
    def __init__(self):
        """Create the CLI.
        """

    def run(self, args: list[str] | None=None) -> int:
        """Run the CLI

        Args:
            args (list[str] | None, optional): Arguments to use. Defaults to sys.argv.

        Returns:
            int: exit code
        """
        # Parse call args
        arg_parser = argparse.ArgumentParser(
            prog=__name__,
            description="A generator for wordle: https://www.nytimes.com/games/wordle/index.html", add_help=True
        )
        arg_parser.add_argument(
            "--highlights-all-duplicate-letters",
            action="store_true",
            help="Set this flag, if your wordle highlights all dublicate letters when only one (ore more) is in word. \
                  If not set, duplicate letters in word get feedback and remaining ones are gray. This is the default.\
                  For the NY Times, omit this flag.",
        )
        arg_parser.add_argument(
            "--language",
            action="store",
            required=False,
            default="",
            type=str,
            help="Set the language (en-english, de-german) of wordle. Asks the user if not given.",
        )
        arg_parser.add_argument(
            "--lenght",
            action="store",
            required=False,
            default=5,
            type=int,
            help="Set the lenght of wordle. Defaults to 5.",
        )
        arg_parser.add_argument(
            "--log-level",
            action="store",
            required=False,
            choices=LOG_LEVEL.keys(),
            default="WARNING",
            help="Set the log level for stdout."
        )
        options = arg_parser.parse_args(args)
        self.options = options

        # Setup and start logging
        # TODO Fix logging (package instead of root logger)
        log = logging.getLogger(__name__).parent
        log.setLevel(logging.DEBUG)

        # stderr logging
        log_console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        log_console_handler = logging.StreamHandler(sys.stdout)
        log_console_handler.setLevel(level=LOG_LEVEL[options.log_level])
        log_console_handler.setFormatter(log_console_formatter)
        log.addHandler(log_console_handler)

        logging.info("Started logging.")

        logging.info(f"Call arguments: {str(options)}")


        # Select language
        language = options.language
        while language not in ("en", "de"):
            language = input(
                "Select the language of the Wordle game (de - deutsch, en - english): "
            ).strip().lower()
        

        # Create wordle bot
        wordleSolver = WordleSolver(
            length=options.lenght,
            language=language,
            highlightsAllDuplicates=options.highlights_all_duplicate_letters,
        )
        
        try:
            while True:
                word = wordleSolver.nextWord()
                # Print the current guess
                print(
                    f"{wordleSolver.round}. "
                    + f"({wordleSolver.guessIndex + 1}/{wordleSolver.lenght}) "
                    + f"WORD: '{word}'"
                )
                
                # Get and parse user feedback
                match self._getUserFeedback():
                    case "q":
                        logging.info("User quit program")
                        return 0
                    case "n" | "next":
                        pass # Loop again
                    case "r":
                        logging.info("User reset program")
                        wordleSolver.reset()
                    case _ as feedback:
                        if wordleSolver.calculate(feedback): # If wordle solved
                            logging.info("Wordle solved")
                            choice = input(
                                'Wordle solved! What do you want do do '
                                +'("q" - quit, "r" - reset and start a new wordle)?\n'
                            ).strip().lower()
                            if choice == "r":
                                logging.info("User reset program")
                                wordleSolver.reset()
                            else:
                                logging.info("User quit program")
                                return 0
                        else: 
                            pass # Loop again
                
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received, exiting")
            return 0
        
    
    def _getUserFeedback(self) -> str:
        """Gets user feedback for the current guessed word

        Returns:
            str: Checked user feedback
        """
        while True:
            user_input = input(
                'What\'s the result? ("-" for grey; "y" for yellow; "g" for green)\n'
                + 'Use "q" to quit and "n" or "next" if word is unknown and "r" to reset.   :'
            ).lower().strip()
            
            # Check if lenght of input the same then lenght of search word
            # and if only chars from the set -yg got used.
            if re.fullmatch(fr"[-yg]{{{self.options.lenght}}}|q|n|next|r", user_input):
                return user_input


if __name__ == "__main__":
# TODO Add stacktrace
#    retCode = 1
#    try:
#        retCode = main()
#    except Exception as e:
#        print(f"Error: {e}", file=sys.stderr)
#    sys.exit(retCode)
    cli = WordleBotCLI()
    sys.exit(cli.run())