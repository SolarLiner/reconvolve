import abc
from argparse import ArgumentParser, Namespace
import logging
import sys
from typing import Dict, List, Optional, Type

from reconvolve import __version__


class BaseCommand(abc.ABC):
    """Base command object from which to implement all subcommands"""
    name: Optional[str]
    description: Optional[str]

    @abc.abstractmethod
    def setup(self, parser: ArgumentParser):
        """Declare arguments and perform one-time setup"""
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self, args: Namespace):
        """Run the subcommand with the aforementioned namespaced arguments"""
        raise NotImplementedError()

    @classmethod
    def get_name(cls):
        if "name" in cls.__dict__ and cls.name is not None:
            return cls.name
        return cls.__class__.__name__

    @classmethod
    def get_description(cls):
        if "description" in cls.__dict__ and cls.description is not None:
            return cls.description
        return cls.__doc__


def setup_parser():
    parser = ArgumentParser(
        description=
        "Create high-quality conolution impulse responses from swept sine waves"
    )
    parser.add_argument("-v", action="count", default=0, help="Increase verbosity")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"$(prog)s {'.'.join(str(v) for v in __version__)}")

    return parser


def setup_logging(verbosity=logging.ERROR):
    logger = logging.getLogger("root")
    sh = logging.StreamHandler()
    sh.setLevel(verbosity)
    logger.addHandler(sh)
    logger.setLevel(verbosity)


def setup(commands: List[BaseCommand]):
    parser = setup_parser()
    subparsers = parser.add_subparsers(title="commands",
                                       help="All available commands")
    cmd_dict: Dict[str, BaseCommand] = dict()
    for cmd in commands:
        name = cmd.get_name()
        subparser = subparsers.add_parser(name, help=cmd.get_description())
        subparser.set_defaults(command_name=name)
        cmd.setup(subparser)
        cmd_dict[name] = cmd

    args = parser.parse_args()
    verbosity = logging.ERROR - args.v * 10
    logger = setup_logging(args.v)
    if "command_name" not in args:
        print("E: You need to call a command.", file=sys.stderr)
        parser.print_usage(sys.stderr)
        exit(1)
    return args, logger, cmd_dict[args.command_name]
