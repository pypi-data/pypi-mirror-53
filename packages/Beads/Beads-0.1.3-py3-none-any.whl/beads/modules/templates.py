from meta import TEMPLATES, supported_languages, file_associations, code_templates, template_keys
from modules.errors import UnsupportedLanguageError
from modules import reader
from string import Template
import logging


def get_template(language: str) -> dict:
    """
    Get the dictionary containing string.Template's for the provided language.

    :param language: string for programming language
    :raises UnsupportedLanguageError if language is not supported
    :return: Dictionary with Templates
    """

    if is_unsupported_language(language):
        raise UnsupportedLanguageError

    template: dict = reader.load_resource(TEMPLATES, code_templates[language])

    for value in template.values():
        for key, string in value.items():
            if key in template_keys:
                value[key] = Template(string)

    return template


def append_language_association(file_name: str, language: str) -> str:
    """
    Append the file_type for the provided language if necessary.

    :param file_name: Filename to append association on.
    :param language: string for programming language
    :raises UnsupportedLanguageError if language is not supported
    :return: File_type for provided language
    """

    if is_unsupported_language(language):
        raise UnsupportedLanguageError

    file_association = file_associations[language]

    if not file_name.endswith(file_association):
        file_name = file_name + file_association

    return file_name


def is_unsupported_language(language: str) -> bool:
    """
    Verify that the given language is supported.
    """

    not_supported = language not in supported_languages

    if not_supported:
        logging.debug(f'TEMPLATES: Identified {language} as not supported')

    return not_supported
