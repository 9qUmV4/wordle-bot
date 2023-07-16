import sys

from .cli import WordleBotCLI

# TODO Add stacktrace
# retCode = 1
# try:
#     retCode = main()
# except Exception as e:
#     print(f"Error: {e}", file=sys.stderr)
# sys.exit(retCode)

cli = WordleBotCLI()
sys.exit(cli.run())
