#!/usr/bin/env python3

# Solver for wordle: https://www.nytimes.com/games/wordle/index.html
# Copyright Illumihax, 9qUmV4

import argparse
import logging
import sys

from .wordleClass import WordleSolver

# Logging
LOG_LEVEL = {
    "CRITICAL": logging.CRITICAL, 
    "ERROR": logging.ERROR, 
    "WARNING": logging.WARNING, 
    "INFO": logging.INFO, 
    "DEBUG": logging.DEBUG
}
    

def main(args=None) -> int:
    # Parse call args
    # arg parsing
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
    
    
    # Run wordle bot
    wordleSolver = WordleSolver(
        length=options.lenght,
        language=options.language if options.language else None,
        highlightsAllDuplicates=options.highlights_all_duplicate_letters,
    )

    try:
        while True:
            match wordleSolver.nextWord():
                case ("SIGNAL:quit"):
                    logging.info("Received SIGNAL:quit")
                    return 0
                case ("SIGNAL:reset"):
                    logging.info("Received SIGNAL:reset")
                    logging.info("Reseting wordleSolver")
                    wordleSolver.reset()
                case ("SIGNAL:wordfound", word):
                    logging.info(f"Received SIGNAL:wordfound (word: {word})")
                    logging.info("Reseting wordleSolver")
                    wordleSolver.reset()
                case ("SIGNAL:newguess", kwargs):
                    logging.info(f"Received SIGNAL:newguess kwargs: {kwargs}")
                case _ as unkwn_sig:
                    logging.critical(f"Unknown signal received: {unkwn_sig}")
                    raise ValueError(f"Unknown signal received: {unkwn_sig}")
                    
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received, exiting")
        return 0

if __name__ == "__main__":
# TODO Add stacktrace
#    retCode = 1
#    try:
#        retCode = main()
#    except Exception as e:
#        print(f"Error: {e}", file=sys.stderr)
#    sys.exit(retCode)
    sys.exit(main())