#!/usr/bin/env python3

# Solver for wordle: https://www.nytimes.com/games/wordle/index.html
# Copyright Illumihax, 9qUmV4

import argparse
import logging
import sys

from wordleClass import WordleSolver

# Logging
LOG_LEVEL = {
    "CRITICAL": logging.CRITICAL, 
    "ERROR": logging.ERROR, 
    "WARNING": logging.WARNING, 
    "INFO": logging.INFO, 
    "DEBUG": logging.DEBUG
}

# arg parsing
arg_parser = argparse.ArgumentParser(description="A generator for wordle: https://www.nytimes.com/games/wordle/index.html", add_help=True)
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


def setup_logging(level:str):
    """Setup and start logging.

    Args:
        level (str): The log level to use.
    """
    log = logging.getLogger(__name__).parent
    log.setLevel(logging.DEBUG)

    # stderr logging
    log_console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    log_console_handler = logging.StreamHandler(sys.stdout)
    log_console_handler.setLevel(level=LOG_LEVEL[level])
    log_console_handler.setFormatter(log_console_formatter)

    log.addHandler(log_console_handler)

    # Say hello
    logging.info("Started logging.")
    

if __name__ == "__main__":
    # Parse call args
    call_args = arg_parser.parse_args()
    
    # Setup and start logging
    setup_logging(call_args.log_level)
    
    logging.info(f"Call arguments: {str(call_args)}")
    
    
    # Run wordle bot
    wordleSolver = WordleSolver(
        length=call_args.lenght,
        language=call_args.language if call_args.language else None
    )

    try:
        while True:
            wordleSolver.nextWord()
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received, exiting")
        sys.exit(0)
