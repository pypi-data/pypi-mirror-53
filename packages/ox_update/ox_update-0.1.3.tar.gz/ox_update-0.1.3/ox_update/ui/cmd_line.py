"""Command line interface to ox_update.
"""

import sys
import logging
import typing

import click

from ox_update import VERSION
from ox_update.checking import shell_checker, common


def prep_sentry(dsn):
    """Prepare sentry if a dsn is passed in.

We do an import inside this function so we do not try to import sentry
if no DSN is given (e.g., if sentry is not installed).
    """
    capture = {'name': 'unknown', 'func': logging.error}

    # pytype gets confused by conditional imports so don't do them
    # if we are in type checking mode
    if not typing.TYPE_CHECKING:
        import sentry_sdk  # pylint: disable=import-error
        sentry_sdk.init(dsn)
        capture = {'name': 'sentry', 'func': sentry_sdk.capture_exception}
    return capture


@click.group()
def main():
    "Command line interface to ox_update."


def add_options(*names):
    """Add options to a click command

    :param *names:   List of strings representing names for options to add.

    ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    :return:  A decorator function to apply to a click command.

    ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    PURPOSE:  For all names provided, look in common.CheckerConfig.options()
              to find option info and then create decorator to put those
              into a click command.

              Basically, this lets you do something like the following:

@click.command()
@add_options('foo', 'bar')
def baz(foo, bar):
    print("foo is %s; bar is %s" % (foo, bar))


    """
    def _add_options(func):
        "Make decorator to apply options to click command."
        info = common.CheckerConfig.options()
        for name in reversed(names):
            option_info = info[name]
            func = click.option(f'--{name}', **option_info)(func)
        return func
    return _add_options


@click.command()
@add_options(*sorted(common.CheckerConfig.options()))
def check(notifiers, age_in_days, sentry, **kwargs):
    "Check to see what needs to be updated."

    capture = {'name': 'logging.error', 'func': logging.error}
    if sentry:
        capture = prep_sentry(sentry)
    try:
        config = common.CheckerConfig(
            updated_age_in_days=age_in_days, notifiers=notifiers, **kwargs)
        checker = shell_checker.SimpleShellChecker(config)
        checker.check()
    except Exception as problem:  # pylint: disable=broad-except
        msg = 'Got Problem: %s' % str(problem)
        if capture:
            msg += '\nWill try to report via %s' % (
                capture.get('name', 'unknown'))
        logging.error(msg)
        capture['func'](problem)
        sys.exit(1)


@click.command()
def version():
    "Shoe version of ox_update."
    msg = 'ox_update version: %s' % VERSION
    click.echo(msg)
    return msg


main.add_command(check)
main.add_command(version)
