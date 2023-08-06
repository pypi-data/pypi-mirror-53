"""A single place for constructing and exposing the main parser
"""

import os
import sys

from ins import __version__
from ins._internal.cli import cmdoptions
from ins._internal.cli.parser import (
    ConfigOptionParser, UpdatingDefaultsHelpFormatter,
)
from ins._internal.commands import (
    commands_dict, get_similar_commands, get_summaries,
)
from ins._internal.exceptions import CommandError
from ins._internal.utils.misc import get_prog
from ins._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from typing import Tuple, List


__all__ = ["create_main_parser", "parse_command"]


def create_main_parser():
    # type: () -> ConfigOptionParser
    """Creates and returns the main parser for ins's CLI
    """

    parser_kw = {
        'usage': '\n%prog <command> [options]',
        'add_help_option': False,
        'formatter': UpdatingDefaultsHelpFormatter(),
        'name': 'global',
        'prog': get_prog(),
    }

    parser = ConfigOptionParser(**parser_kw)
    parser.disable_interspersed_args()

    ins_pkg_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..",
    ))
    parser.version = 'ins %s from %s (python %s)' % (
        __version__, ins_pkg_dir, sys.version[:3],
    )

    # add the general options
    gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, parser)
    parser.add_option_group(gen_opts)

    # so the help formatter knows
    parser.main = True  # type: ignore

    # create command listing for description
    command_summaries = get_summaries()
    description = [''] + ['%-27s %s' % (i, j) for i, j in command_summaries]
    parser.description = '\n'.join(description)

    return parser


def parse_command(args):
    # type: (List[str]) -> Tuple[str, List[str]]
    parser = create_main_parser()

    # Note: parser calls disable_interspersed_args(), so the result of this
    # call is to split the initial args into the general options before the
    # subcommand and everything else.
    # For example:
    #  args: ['--timeout=5', 'install', '--user', 'INITools']
    #  general_options: ['--timeout==5']
    #  args_else: ['install', '--user', 'INITools']
    general_options, args_else = parser.parse_args(args)

    # --version
    if general_options.version:
        sys.stdout.write(parser.version)  # type: ignore
        sys.stdout.write(os.linesep)
        sys.exit()

    # ins || ins help -> print_help()
    if not args_else or (args_else[0] == 'help' and len(args_else) == 1):
        parser.print_help()
        sys.exit()

    # the subcommand name
    cmd_name = args_else[0]

    if cmd_name not in commands_dict:
        guess = get_similar_commands(cmd_name)

        msg = ['unknown command "%s"' % cmd_name]
        if guess:
            msg.append('maybe you meant "%s"' % guess)

        raise CommandError(' - '.join(msg))

    # all the args without the subcommand
    cmd_args = args[:]
    cmd_args.remove(cmd_name)

    return cmd_name, cmd_args
