#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# This software is distributed under the terms of the MIT License.
#
#                                       (@@@@%%%%%%%%%&@@&.
#                              /%&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&@@(
#                              *@&%%%%%%%%%&&%%%%%%%%%%%%%%%%%%&&&%%%%%%%
#                               @   @@@(@@@@%%%%%%%%%%%%%%%%&@@&* @@@   .
#                               ,   .        .  .@@@&                   /
#                                .       .                              *
#                               @@              .                       @
#                              @&&&&&&@. .    .                     *@%&@
#                              &&&&&&&&&&&&&&&&@@        *@@############@
#                     *&/ @@ #&&&&&&&&&&&&&&&&&&&&@  ###################*
#                              @&&&&&&&&&&&&&&&&&&##################@
#                                 %@&&&&&&&&&&&&&&################@
#                                        @&&&&&&&&&&%#######&@%
#  nanaimo                                   (@&&&&####@@*
#
import argparse
import asyncio
import logging
import sys
import typing
import nanaimo


class CreateAndGatherFunctor:
    """
    Stores the type, manager, and loop then uses these to instantiate
    and invoke a Fixture if the given default is selected.
    Returns the result-code of the artifacts.
    """

    def __init__(self, fixture_type: typing.Type['nanaimo.Fixture'], manager: nanaimo.FixtureManager, loop: asyncio.AbstractEventLoop):
        self._fixture_type = fixture_type
        self._manager = manager
        self._loop = loop

    async def __call__(self, args: nanaimo.Namespace) -> int:
        fixture = self._fixture_type(self._manager, self._loop)
        return int(await fixture.gather(args))


class _ArgparseSubparserArguments(nanaimo.Arguments):
    """
    Nanaimo :class:`Arguments` that delegates to a wrapped
    :class:`argparse.ArgumentParser` instance.
    """

    @classmethod
    def visit_argparse(cls,
                       manager: nanaimo.FixtureManager,
                       subparsers: argparse._SubParsersAction,
                       loop: asyncio.AbstractEventLoop) -> None:
        for fixture_type in manager.fixture_types():
            subparser = subparsers.add_parser(fixture_type.get_canonical_name())  # type: 'argparse.ArgumentParser'
            subparser.add_argument('--test-timeout-seconds',
                                   default='30',
                                   type=float,
                                   help='''Test will be killed and marked as a failure after
waiting for a result for this amount of time.''')
            fixture_type.on_visit_test_arguments(cls(subparser))
            subparser.set_defaults(func=CreateAndGatherFunctor(fixture_type, manager, loop))

    def __init__(self, subparser: argparse.ArgumentParser):
        self._subparser = subparser

    def add_argument(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._subparser.add_argument(*args, **kwargs)

    def set_defaults(self, **kwargs: typing.Any) -> None:
        self._subparser.set_defaults(**kwargs)


def _make_parser(loop: typing.Optional[asyncio.AbstractEventLoop] = None) -> argparse.ArgumentParser:
    """
    Defines the command-line interface. Provided as a separate factory method to
    support sphinx-argparse documentation.
    """

    epilog = '''**Example Usage**::

    python -m nanaimo -vv nanaimo_bar

----
'''

    parser = argparse.ArgumentParser(
        description='Run tests against hardware.',
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter)

    from nanaimo.version import __version__

    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('--verbose', '-v', action='count',
                        help='verbosity level (-v, -vv)')

    subparsers = parser.add_subparsers(help='sub-command help')

    pm = nanaimo.FixtureManager()

    _ArgparseSubparserArguments.visit_argparse(pm, subparsers, loop)  # type: ignore

    return parser


def _setup_logging(args: argparse.Namespace) -> None:
    fmt = '%(name)s : %(message)s'
    level = {0: logging.WARNING, 1: logging.INFO,
             2: logging.DEBUG}.get(args.verbose or 0, logging.DEBUG)
    logging.basicConfig(stream=sys.stderr, level=level, format=fmt)
    if args.verbose is not None and args.verbose >= 3:
        logging.getLogger('asyncio').setLevel(logging.DEBUG)


def main() -> int:
    """
    CLI entrypoint for running Nanaimo tests.
    """

    loop = asyncio.get_event_loop()

    parser = _make_parser(loop)
    args = parser.parse_args()

    _setup_logging(args)

    if hasattr(args, 'func'):
        result = loop.run_until_complete(args.func(nanaimo.Namespace(args)))
        try:
            return int(result)
        except ValueError:
            print('Nanaimo tests must return an int result!')
            raise
    else:
        parser.print_usage()
        return -1
