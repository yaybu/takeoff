import argparse
import logging
import sys

from touchdown.frontends import ConsoleFrontend
from touchdown.core.main import configure_parser

from takeoff.workspace import Takeofffile


def main(argv=None):
    parser = argparse.ArgumentParser(description="Manage your infrastructure")
    console = ConsoleFrontend()
    configure_parser(parser, Takeofffile(), console)
    args = parser.parse_args(argv or sys.argv[1:])

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(name)s: %(message)s")

    console.interactive = not args.unattended

    args.func(args)


if __name__ == "__main__":
    main()
