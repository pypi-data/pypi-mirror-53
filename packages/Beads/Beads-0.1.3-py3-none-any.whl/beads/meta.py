from os import path, listdir

# General
VERSION: str = '0.1.3'
TOOL_NAME: str = 'Beads'


# De-/Encoding
STANDARD_ENCODING: str = 'UTF8'


# Paths
ROOT_DIR: str = path.dirname(path.abspath(__file__))
RESOURCES_PATH: str = path.join(ROOT_DIR, 'resources')
GUI_PATH: str = path.join(RESOURCES_PATH, 'ui')
HTML: str = 'index.html'

# Resource sub directories
TEMPLATES: str = 'templates'
OPTION_SUB_DIR: str = 'options'

# Default-Options
DEFAULT_OPTIONS: str = 'default_options.json'

# CLI
NO_WINDOW: str = 'no-window'
PORT: str = 'port'
SKIP_VALIDATION: str = 'skip-validation'
VERBOSE: str = 'verbose'
REPLACE: str = 'replace-existing'
OUT_DIR: str = 'out-dir'
FILENAME: str = 'filename'

help_no_window: str = 'Run the gui without opening a browser window.'
help_file_gui: str = 'Load provided FILE after setup.'
help_port: str = 'Specify the PORT to run the gui on.'
help_languages: str = 'Programming language to use for code generation.'
help_no_validation: str = 'Disable validation of provided fine state machine.'
help_verbose: str = 'Run command in verbose mode printing all debugging information.'
help_out_dir: str = 'Specify DIRECTORY to write output files into.'
help_compile_name: str = 'Specify the NAME of the output file without ending.'
help_replace_existing: str = 'Automatically replace existing files with same name.'
help_set_option: str = 'Set a default runtime option: OPTION VALUE'
help_unset_option: str = 'Delete a default runtime option: OPTION'
help_unset_all: str = 'Delete all default runtime options.'
help_show_options: str = 'Show all available default options.'


# FSMs
NODES: str = 'nodes'
START: str = 'start'
TRANSITIONS: str = 'transitions'
ID = 'id'
VALUE = 'value'
LABEL: str = 'label'
FROM: str = 'from'
TO: str = 'to'


# Templates
CONFIG: str = 'config'
USE_HEADER: str = "useHeader"
GAP: str = 'gap'
INDENT: str = 'indent'
NAME: str = 'name'
BODY: str = 'body'
ITEM: str = 'item'
ITEM_FIRST: str = 'item_first'
STATES: str = 'states'
STATE: str = 'state'
HEADER: str = 'header'
FOOTER: str = 'footer'

template_keys: set = {BODY, ITEM, ITEM_FIRST, "content"}
TEMPLATE_FILE: str = '.template'
LANGUAGE: str = 'language'
FILE_TYPE: str = 'file_type'
TEMPLATE_VERSION: str = 'version'
TEMPLATE_VERSIONS: set = {'1'}

CONTENT: str = 'content'
MODE: str = 'mode'

# Programming languages
supported_languages: set = set()
code_templates: dict = dict()
file_associations: dict = dict()


def __find_languages__() -> None:
    """
    Find and set all supported languages via the existence of a valid template
    """
    from modules.reader import read_config

    global supported_languages
    global code_templates
    global file_associations

    for file_path in __gather_template_files__():

        with open(file_path) as content:

            first_line = content.readline()
            if first_line.startswith('#!'):

                config: dict = read_config(first_line)

                if __is_valid_config__(config):
                    language = config[LANGUAGE]
                    supported_languages.add(language)
                    code_templates.update({language: ''.join([language, TEMPLATE_FILE])})
                    file_associations.update({language: config[FILE_TYPE]})


def __is_valid_config__(config: dict) -> bool:
    """
    Verify that all needed keys are present and the declared version is supported

    :param config: Dictionary with configuration key:values
    :return: True if verified, otherwise False
    """

    required_keys = [TEMPLATE_VERSION, LANGUAGE, TEMPLATE_FILE, FILE_TYPE]

    return [key in config.keys() for key in required_keys] and config[TEMPLATE_VERSION] in TEMPLATE_VERSIONS


def __gather_template_files__() -> list:
    """
    Generator for file_paths of template files.

    :return: File_paths that are files and end with '.template'
    """
    templates_path = path.join(RESOURCES_PATH, TEMPLATES)

    for file in listdir(templates_path):

        file_path: str = path.join(templates_path, file)

        if path.isfile(file_path) and file.endswith(TEMPLATE_FILE):
            yield file_path


__find_languages__()
