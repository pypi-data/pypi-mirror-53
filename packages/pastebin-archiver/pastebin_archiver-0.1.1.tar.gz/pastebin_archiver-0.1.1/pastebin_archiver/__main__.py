import argparse
import logging
import sys

from pastebin_archiver import PastebinArchiver
from pastebin_archiver import Config


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--loglevel",
        dest="loglevel",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="set the logging level",
    )
    parser.add_argument(
        "--logfile",
        dest="logfile",
        default=f"pastebin-archiver.log",
        help="set a file to append logs to",
    )
    parser.add_argument(
        "--database",
        dest="db_string",
        default="sqlite:///pastebin.db",
        help="set the database connection string",
    )
    args = parser.parse_args()
    Config.db_connection_string = args.db_string

    # Configure logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter("{message}", style="{"))
    file_handler = logging.FileHandler(args.logfile)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "{asctime} {levelname} \t{name}: {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger = logging.getLogger("pastebin_archiver")
    logger.setLevel(getattr(logging, args.loglevel))
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Run the application
    app = PastebinArchiver()
    try:
        app.main()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit()


if __name__ == "__main__":
    main()
