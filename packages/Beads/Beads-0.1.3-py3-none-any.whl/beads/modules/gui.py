from meta import *
from modules.logic import process
from modules.errors import ParsingError, ValidationError, UnsupportedLanguageError
from modules import defaults, reader
from typing import IO
from distutils.util import strtobool
import logging
import eel
import json

browser_options: dict = {
    'window_size': (1200, 800),
    'extensions': ['.js', '.html'],
}

file_to_load: dict or None = None


def start(file: IO, opts: dict) -> None:
    """
    Start the local server for the Graphical User Interface.

    Method utilizing eel library to provide entry point for a GUI.
    If given FILE is None the GUI will start empty.

    :param file: File to open on start or None
    :param opts: Dictionary with available gui options
    """

    startup_options = {
        PORT: opts[PORT]
    }

    if file:
        global file_to_load
        file_to_load = reader.parse_file(file)

    eel.init(GUI_PATH, allowed_extensions=browser_options['extensions'])

    if opts[NO_WINDOW]:
        startup_options[MODE] = None

    try:
        eel.start(HTML, options=startup_options, size=browser_options['window_size'])

    except Exception:
        startup_options[MODE] = 'edge'
        eel.start(HTML, options=startup_options, size=browser_options['window_size'])


"""     GUI API

    API for the graphical user interface provided with web technologies.

    All functions listed below that are annotated with @eel.expose can be called on javascript side
    via the exposed 'eel' object.

"""


@eel.expose
def parse(graph: str, language: str, opts: str) -> (str, str):
    """
    Parse the given json string in the provided language and generate code.

    :param graph: fsm as json
    :param language: Programming language to use for code generation
    :param opts: JSON string of available options
    """

    logging.debug(f'GUI: parse called with JSON: {graph} and language: {language}')
    logging.debug(f'GUI: provided options: {opts}')

    code: str or None = None
    error: str or None = None

    try:
        fsm: dict = json.loads(graph)
        logging.debug(f'GUI: Parsed provided GRAPH into state machine:\n {fsm}')

        options: dict = json.loads(opts)
        logging.debug(f'GUI: Parsed provided OPTS into options:\n {options}')

        skip_validation = options[SKIP_VALIDATION]
        if type(skip_validation) is str:
            skip_validation = bool(strtobool(skip_validation))

        if skip_validation:
            logging.debug('GUI: Validation of internal logic will be skipped!')

        code = process(fsm, language, skip_validation)
        logging.debug(f'GUI: Processed state machine to code:\n{code}')

    except ParsingError as pe:
        error = f'Content could not be parsed into a valid format!\n{pe.cause}'
    except ValidationError as ve:
        error = f'Validation of state machine logic failed: {ve.cause}'
    except UnsupportedLanguageError:
        error = f'Provided language: "{language}" is not supported!'

    if error is not None:
        logging.error(f'GUI: {error}')
        logging.warning('GUI: Code generation aborted. Returning error!')

    return code, error


@eel.expose
def load_file() -> str:
    """
    Send the file to load to the GUI.
    """

    return json.dumps(file_to_load)


@eel.expose
def set_option(key: str, value: str) -> None:
    """
    Set options via GUI.
    """

    if defaults.set_default(key, value):
        defaults.save()


@eel.expose
def unset_option(key: str) -> None:
    """
    Unset options via GUI.
    """

    if defaults.unset_default(key):
        defaults.save()


@eel.expose
def unset_all_options() -> None:
    """
    Unset all options via GUI.
    """
    
    return defaults.unset_all()


@eel.expose
def available_languages() -> str:
    """
    Provide all available languages to the GUI.
    """

    return json.dumps({'languages': [lang for lang in supported_languages]})


@eel.expose
def available_defaults() -> str:
    """
    Provide all available defaults to the GUI.

    Defaults follow the schema below:

        [key: string]: {
            'typevalue': any,
            'current': any,
            'description': string
        }

    """
    current: dict = defaults.current_defaults
    descriptions: dict = defaults.keys_help

    processed: dict = {}

    for key, value in defaults.keys_values.items():
        if value is str:
            value = ''
        elif value is bool:
            value = False
        elif value is int:
            value = 0

        processed[key] = {
            'typevalue': value,
            'current': current[key] if key in current else None,
            'description': descriptions[key]
        }

    try:
        return json.dumps(processed)

    except TypeError as te:
        logging.warning(f'GUI: json error: {te}')


@eel.expose
def get_version() -> str:
    """
    Provide version information to the GUI.
    """

    return VERSION


@eel.expose
def get_info() -> str:
    """
    Provide tool documentation the GUI.
    """

    resource: dict = reader.load_resource('info', 'README.md')

    return json.dumps(resource[CONTENT])
