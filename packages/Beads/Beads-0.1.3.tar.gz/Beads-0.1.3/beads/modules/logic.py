from modules.errors import ValidationError, UnsupportedLanguageError
from modules.generator import CodeGenerator
from modules import templates, validator
import logging


def process(fsm: dict, language: str, skip_validation: bool = False) -> str:
    """
    Process the FSM in the given LANGUAGE.

    Set SKIP_VALIDATION argument to True if validation of internal fsm logic shall be skipped.
    Process pipeline will first validate the internal fsm logic and then generate code based on
    a template for the given language.

    :param fsm: Fine State Machine parsed to Dictionary
    :param language: String for programming language to use as base for code generation
    :param skip_validation: Flag to skip validation of fsm logic
    :return: Code string representing the provided fine state machine
    """

    logging.debug('LOGIC: Starting to parse Fine State Machine')

    try:
        if skip_validation:
            logging.debug('LOGIC: Skip validation of state machine logic')

        else:
            logging.debug('LOGIC: Start validation of state machine')
            validator.inspect(fsm)
            logging.debug('LOGIC: Validation of state machine logic successful')

        template: dict = templates.get_template(language)
        logging.debug(f'LOGIC: For language: "{language}" got template:\n{template}')

        code = CodeGenerator(template).build(fsm)
        logging.debug(f'LOGIC: Code generation ran successful.')

        logging.debug('LOGIC: Finished to parse Fine State Machine')
        return code

    except ValidationError as ve:
        raise ve
    except UnsupportedLanguageError as ule:
        raise ule
