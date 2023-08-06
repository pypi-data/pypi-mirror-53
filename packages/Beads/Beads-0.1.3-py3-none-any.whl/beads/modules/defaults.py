from meta import *
from modules import reader, writer
from distutils.util import strtobool
import logging


def set_default(option: str, value: str) -> bool:
    """
    Set a default runtime OPTION to the provided VALUE.

    Automatically handles int and bool values if needed.

    :param option: The OPTION to set the value for
    :param value: Value as string to set the OPTION to
    :return: True if option was successfully set, otherwise False
    """

    success: bool = False

    if option in keys_values.keys():
        new_value = value_for_key(option, value)

        if new_value is not None:
            current_defaults[option] = new_value
            logging.debug(f'DEFAULTS: Set {option} to {new_value}.')
            success = True

    return success


def unset_default(option: str) -> bool:
    """
    Un-set a default runtime OPTION.

    :param option: The OPTION to unset
    :return: True if option was successfully unset, otherwise False
    """

    success: bool = False

    if option in keys_values.keys():
        try:
            del current_defaults[option]
            logging.debug(f'DEFAULTS: Unset {option}')
            success = True

        except KeyError:
            pass

    return success


def unset_all() -> None:
    """
    Unset all currently saved default runtime options.

    Method will save the empty default-options!
    """

    writer.save_resource(OPTION_SUB_DIR, DEFAULT_OPTIONS, {})


def save() -> None:
    """
    Persist the currently set default runtime options.
    """

    writer.save_resource(OPTION_SUB_DIR, DEFAULT_OPTIONS, current_defaults)


def get(key: str, value_on_none: str or int or bool) -> str or int or bool:
    """
    Get the default value for the provided runtime option as KEY.
    If no such value is present the VALUE_ON_NONE will be returned.

    :param key: Runtime Option key to get value for
    :param value_on_none: Value for Option (KEY)
    :return: Set default value or VALUE_ON_NONE if none found
    """

    default_value = value_on_none

    if key in current_defaults:
        default_value = current_defaults[key]

    return default_value


def load_defaults() -> dict:
    """
    Load the saved defaults for runtime options.

    :return: Dictionary of defaults or empty if none could be found.
    """

    defaults: dict = {}

    for key, value in reader.load_resource(OPTION_SUB_DIR, DEFAULT_OPTIONS).items():
        if key in keys_values:
            value_to_set = value_for_key(key, value)

            if value_to_set is not None:
                defaults[key] = value_to_set

    return defaults


def value_for_key(key: str, value) -> str or int or bool or None:
    """
    Parse the provided value into the required form the the given key.

    Will return None if any problems occur.

    :param key: Key string for default options.
    :param value: Value to parse
    :return: Parsed value or None
    """
    new_value = None

    try:
        option_type = keys_values[key]

        if option_type is int:
            new_value = int(value)

        elif option_type is bool:
            if type(value) is str:
                value = strtobool(value)

            new_value = bool(value)

        elif option_type is str:
            new_value = str(value)

    except ValueError:
        logging.debug(f'DEFAULTS: Could not parse "{value}" into required form for key "{key}"!')

    return new_value


keys_values: dict = {
    LANGUAGE: str,
    NO_WINDOW: bool,
    OUT_DIR: str,
    PORT: int,
    REPLACE: bool,
    SKIP_VALIDATION: bool,
    VERBOSE: bool,
}

keys_help: dict = {
    LANGUAGE: help_languages,
    NO_WINDOW: f'{help_no_window} Requires new start to take effect.',
    OUT_DIR: help_out_dir,
    PORT: f'{help_port} Requires new start to take effect.',
    REPLACE: help_replace_existing,
    SKIP_VALIDATION: help_no_validation,
    VERBOSE: f'{help_verbose} Requires new start to take effect.'
}

current_defaults: dict = load_defaults()
