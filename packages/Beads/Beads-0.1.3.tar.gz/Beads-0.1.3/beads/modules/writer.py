from modules.errors import ExistingFileError
from meta import RESOURCES_PATH
import logging
import json
import os


def save_text_file(text: str, path: str, overwrite_existing: bool = False) -> None:
    """
    Write the provided TEXT into a file with given PATH.

    Will only overwrite already existing files if OVERWRITE_EXISTING is True.

    :param text: Content to save
    :param path: File path to save into
    :param overwrite_existing: Flag to specify overwriting of existing files
    :raises ExistingFileError if file with PATH exists but OVERWRITE_EXISTING is False
    :raises IOError
    """

    if overwrite_existing:
        overwrite(text, path)

    else:
        try:
            open(path)
            logging.debug(f'WRITER: file with path {path} could be opened. File exists')
            raise ExistingFileError

        except IOError:
            overwrite(text, path)


def save_resource(subdir: str, name: str, full_content: dict) -> None:
    """
    Write the provided FULL_CONTENT into a file with given NAME.

    :param subdir: Sub directory of the resources folder
    :param name: Filename
    :param full_content: Full resources content as dict
    """

    resource_path: str = os.path.join(RESOURCES_PATH, subdir, name)

    content: str = json.dumps(full_content)

    save_text_file(content, resource_path, True)


def overwrite(text: str, path: str) -> None:
    """
    Write TEXT into PATH in 'w+' mode.
    Will overwrite existing files!

    :param text: Content to write/save
    :param path: PATH to save into
    :raises IOError
    """

    out_dir: str = os.path.dirname(path)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    output_file = open(path, 'w+')
    output_file.write(text)
    output_file.close()

    logging.debug(f'WRITER: Writing successful for file: {path}')

