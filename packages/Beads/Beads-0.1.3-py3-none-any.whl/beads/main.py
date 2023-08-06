from meta import *
from modules import defaults, cli, gui as gui_handler
from modules.clicklog import Overview, info, warn
from typing import IO
import datetime
import logging
import click
import os


@click.group()
@click.version_option(version=VERSION, prog_name=TOOL_NAME)
def beads() -> None:
    """
    Simple Code generation tool parsing fine state machines and transpiling them into code snippets.

    Beads provides a commandline interface and a graphical user interface (GUI) via their
    respective commands.

    Provide or draw a fine state machine (fsm) and code corresponding to the fsm will be generated. An overview of all
    supported programming languages can be printed using the 'languages' command on the commandline,
    or viewed under 'Settings' in the GUI.

    The list of all available command and options to use this tool can be found online:
    https://gitlab.beuth-hochschule.de/s40242/stategen/blob/master/README.md

    and on the commandline upon providing the '--help' option like so: 'beads --help' or 'beads [any command] --help'
    for each sub-command respectively.

    The GUI also provides a readme and help section here: 'Menu' > 'Tool Info'
    """

    pass


@beads.command()
@click.option('-b', '--background', 'no_window', flag_value=True, help=help_no_window)
@click.option('-p', '--port', type=click.INT, default=None, help=help_port)
@click.option('-v', '--verbose', 'is_verbose', flag_value=True, help=help_verbose)
@click.option('--file', type=click.File(mode='r'), default=None, help=help_file_gui)
def gui(no_window: bool, port: int,  is_verbose: bool, file: IO) -> None:
    """
    Open a graphical user interface (GUI).

    The GUI allows drawing of fine state machines and provides means to set/change user specific default settings
    that are considered in commandline usage as well.
    """

    opts = dict()
    opts[NO_WINDOW] = no_window or defaults.get(NO_WINDOW, False)
    opts[PORT] = port or defaults.get(PORT, 8000)

    set_up_logger(is_verbose)

    gui_handler.start(file, opts)


@beads.command()
@click.option('-l', '--language', type=click.Choice(supported_languages), default=None, help=help_languages)
@click.option('-nv', '--no-validation', flag_value=True, help=help_no_validation)
@click.option('-o', '--out', 'file_name', type=str, default=None, help=help_compile_name)
@click.option('-bd', '--base-directory', type=click.Path(exists=True, file_okay=False), default=None, help=help_out_dir)
@click.option('-re', '--replace-existing', 'replace', flag_value=True, help=help_replace_existing)
@click.option('-v', '--verbose', 'is_verbose', flag_value=True, help=help_verbose)
@click.argument('files', type=click.File(mode='r'), nargs=-1, required=True)
def parse(files: list, language: str, no_validation: bool, is_verbose: bool,
          base_directory: str, file_name: str, replace: bool) -> None:
    """
    Parse a provided FILE into code.

    Parse the provided FILE containing a textual representation of a fine state machine
    and generate a code snippet representing this machines internal logic.
    """

    set_up_logger(is_verbose)

    opts = dict()
    opts[SKIP_VALIDATION] = no_validation or defaults.get(SKIP_VALIDATION, False)
    opts[REPLACE] = replace or defaults.get(REPLACE, False)
    opts[OUT_DIR] = base_directory or defaults.get(OUT_DIR, os.getcwd())

    language = language or defaults.get(LANGUAGE, None)

    if len(files) == 1:
        file = files[0]

        opts[FILENAME] = file_name or default_file_name(file)

        cli.parse(file, language, opts)

    else:
        for file in files:
            opts[FILENAME] = default_file_name(file)

            cli.parse(file, language, opts)


@beads.command()
@click.argument('search_text', type=str, default=None, required=False)
def languages(search_text: str) -> None:
    """
    Print an overview of all supported programming languages.

    Languages can be filter by providing a SEARCH_TEXT to look for.

    :param search_text: String that is contained in language name or None
    """

    end: str = f' with "{search_text}"' if search_text is not None else ''
    title: str = f'Supported programming languages{end}'

    overview: Overview = Overview(title)
    overview.print(f'*   {language}' for language in filter_languages(search_text))


@beads.command()
@click.option('-s', '--set-default', 'options_to_set', type=(str, str), multiple=True, help=help_set_option)
@click.option('-u', '--unset-default', 'options_to_unset', type=str, multiple=True, help=help_unset_option)
@click.option('--unset-all', flag_value=True, help=help_unset_all)
@click.option('--show', flag_value=True, help=help_show_options)
def options(options_to_set: list, options_to_unset: list, unset_all: bool, show: bool) -> None:
    """
    Print an overview of all currently set default runtime options.

    Allows to view, set and unset options that are used by default.
    Provide --show to print a list of all available options and their value types.

    Use -s/--set as:   --set language python

    Use -u/--unset as:    --unset language

    Setting and Un-setting of options can be provided multiple times for one call.
    The options take the following precedence:

        1. If unset-all is given, set and unset will be ignored!

        2. Setting is done before un-setting!

        3. --show will be executed independently
    """

    if show:
        overview: Overview = Overview('Available default runtime options')
        overview.print(f'  {key}: {value.__name__}' for key, value in defaults.keys_values.items())

    if unset_all:
        if click.confirm('Delete all currently set default options?'):
            defaults.unset_all()
            info('Deleted all runtime default options.')
        else:
            info('Aborted!')

    elif len(options_to_set) > 0 or len(options_to_unset) > 0:
        for option, value in options_to_set:
            if defaults.set_default(option, value):
                info(f'Set --{option} to {value}!')
            else:
                warn(f'Could not set --{option} to {value}')

        for option in options_to_unset:
            if defaults.unset_default(option):
                info(f'Unset option --{option}!')
            else:
                warn(f'Could not unset --{option}')

        defaults.save()

    else:
        if len(defaults.current_defaults) == 0:
            info('There are no default runtime options set!')

        else:
            overview: Overview = Overview('Current default runtime options')
            overview.print(f'  --{key} {value}' for key, value in defaults.current_defaults.items())


def set_up_logger(verbose: bool) -> None:
    """
    Set up logging for program execution.

    Provide 'verbose' as True to set 'DEBUG' logging level.

    :param verbose: Debug flag
    """

    is_verbose = verbose or defaults.get(VERBOSE, False)

    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    log_level = logging.DEBUG if is_verbose else logging.WARNING
    logging.basicConfig(level=log_level)
    logging.debug(f'MAIN: Set up logger with level={log_level}')


def default_file_name(file: IO) -> str:
    """
    Get the default name for an input file

    :param file: IO user input
    :return: default name for file
    """

    default_name = file.name.rpartition('.')[0]

    if default_name == '':
        default_name = f'generated_code_{str(datetime.datetime.now())}'

    return default_name


def filter_languages(search_text: str) -> iter:
    """
    Filter all supported languages by given SEARCH_TEXT.

    :param search_text: String to look for in supported languages
    :return: ALl languages that contain the search_text.
    """

    for language in sorted(supported_languages):
        if search_text is None or search_text in language:
            yield language


if __name__ == '__main__':
    exit(beads())
