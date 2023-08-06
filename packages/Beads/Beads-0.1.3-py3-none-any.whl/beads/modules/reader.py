from meta import *
from modules.errors import ParsingError
from typing import IO
import markdown as md
import logging
import json
import os


def parse_file(file: IO) -> dict:
    """
    Parse the provided file into a dictionary.

    Method to parse input files into an internally usable version (dict).
    All supported file formats can be found here: TODO
    To parse string / text use 'parse_text' instead!

    :param file: IO to parse
    :return: Dictionary containing the file contents
    """

    if file.name.endswith('.json'):
        logging.debug(f'READER: Identified {file.name} as json: Calling json.load')
        content = json.load(file)

    elif file.name.endswith('.bead'):
        logging.debug(f'READER: Identified {file.name} as beads-file: parsing from bds to json')
        content = parse_beads(file)

    else:
        raise ParsingError('Unsupported file-type!')

    logging.debug(f'READER: Parsed file: {file.name} to :\n{content}')

    return content


def parse_text(text: str) -> dict:
    """
    Parse the provided text / string into a dictionary.

    Method to parse input text / str into an internally usable version (dict).
    All supported text formats can be found here: TODO
    To parse files use 'parse_file' instead!

    :param text: Text / string to parse
    :return: Dictionary containing the string contents
    """

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        raise ParsingError


def parse_beads(file: IO) -> dict:
    """
    Parse the provided Beads file into a dictionary.

    Method to parse input file into an internally usable version (dict).

    :param file: IO to parse
    :return: Dictionary containing the string contents
    """

    graph_name: str = 'graph'
    nodes: set = set()
    initial_node: str or None = None
    transitions: list = []

    first_line = file.readline()
    file.seek(0)

    if first_line.strip().startswith('#!'):
        config = read_config(first_line)

        if START in config.keys():
            initial_node = config[START]

        if NAME in config.keys():
            graph_name = config[NAME]

    if initial_node is not None:
        nodes.add(initial_node)

    for line in strip_comments(file):
        [_from, transition, _to] = decode_line(line)
        transition = {LABEL: transition, FROM: _from, TO: _to}

        transitions.append(transition)
        nodes.add(_from)
        nodes.add(_to)

    content = {
        NAME: graph_name,
        NODES: wrap_node_names(nodes, initial_node),
        TRANSITIONS: transitions
    }

    return content


def decode_line(transition: str) -> tuple:
    """
    Decode a line of a .bead file

    :param transition: str - line to validate
    :return: list of names for LABEL, FROM and TO
    """

    try:
        trans_strings = transition.strip().split(':')

        # assert transition string has valid structure
        assert len(trans_strings) == 3,\
            f'Invalid transition format\n expected: state_from:transition:state_to\n got: {transition}'

        trans_strings = (trans_strings[0].strip(), trans_strings[1].strip(), trans_strings[2].strip())

        # assert names are valid
        for string in trans_strings:
            for char in string:
                assert char.isalnum() or char == '_',\
                    f'Invalid sign "{char}" in "{string}":\nUse only alphanumeric signs (a - Z, 0 - 9) and "_"'

    except AssertionError as ae:
        logging.debug(f'READER: Decoding of {transition} failed!')
        raise ParsingError(ae)

    return trans_strings


def wrap_node_names(nodes: set, initial_node: str or None) -> list:
    """
    Wrap all node names into required dicts.

    :param initial_node: Optional node defining starting point
    :param nodes: Set of node names
    """

    nodes_list: list = []

    for node_name in sorted(nodes):
        node = {ID: node_name}

        if initial_node and node_name == initial_node:
            node[START] = True

        nodes_list.append(node)

    return nodes_list


def load_resource(subdir: str, name: str) -> dict:
    """
    Load a resource and provide the content as a DICT.

    This method will load a resource json file from the provided SUBDIR (directory)

    :param subdir: Subdirectory the resource is located in
    :param name: Filename of the resource
    :return: A parsed dictionary of the specified resource
    """

    resource_path = os.path.join(RESOURCES_PATH, subdir, name)
    logging.debug(f'READER: Constructed resource_path: {resource_path}')

    res: dict = {}
    if name.endswith(".json") or name.endswith(".template"):
        with open(resource_path, encoding=STANDARD_ENCODING) as resource:
            content: str = ''.join(strip_comments(resource))
            logging.debug(f'READER: Read content: {content}')

            res = json.loads(content)

    elif name.endswith(".md"):

        with open(resource_path, encoding=STANDARD_ENCODING) as resource:
            content: str = md.markdown(resource.read(), extensions=['fenced_code'])
            logging.debug(f'READER: Read content: {content}')

        res[CONTENT] = content

    logging.debug(f'READER: Loaded resource as: {res}')

    return res


def read_config(line: str) -> dict:
    """
    Read the config line of a file.

    Config lines start with #! and declare configuration item like name:value.
    Items need to be separated by whitespace.

    :param line: Config line as str
    :return: parsed config as dict
    """

    config: dict = {}

    config_list: list = line.split(' ')

    for element in config_list:
        if ':' in element:
            item = element.split(':')
            config.update({item[0]: item[1].replace('\n', '')})

    return config


def strip_comments(file: IO) -> str:
    """
    Clear a resource file of comments.

    This method will return a generator object yielding only lines that are striped from comments.
    Comments are cleared like so:
        # Comments outside will be cleared
        {
            # Single line comments inside will be cleared
            "key":"value" # Trailing comments will be cleared

            "key": # This will result in an error "value"
            "key#": This will result in an error "value"
            "key": "val '# This will also result in an error' ue"
        }

    :param file: Resource file to strip comments from
    :return: Generator for str
    """

    for line in file.readlines():
        line = line.partition('#')[0].rstrip()
        if line:
            yield line
