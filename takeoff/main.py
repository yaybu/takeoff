import argparse
import logging
import sys

from touchdown.frontends import ConsoleFrontend
from touchdown.core.main import configure_parser

from takeoff.workspace import Takeofffile
from takeoff.goal import BuildWorkspace


def get_default_workspace():
    workspace = Takeofffile()
    workspace.load()
    return workspace


def main(argv=None):
    parser = argparse.ArgumentParser(description="Manage your infrastructure")

    console = ConsoleFrontend()
    workspace = BuildWorkspace(get_default_workspace(), console).execute()
    configure_parser(parser, workspace, console)

    args = parser.parse_args(argv or sys.argv[1:])

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(name)s: %(message)s")

    console.interactive = not args.unattended

    args.func(args)


if __name__ == "__main__":
    main()
