from meta import SKIP_VALIDATION, FILENAME, REPLACE, OUT_DIR, NAME
from modules.logic import process
from modules.templates import append_language_association
from modules.errors import ParsingError, InternalException, ExistingFileError, ValidationError, UnsupportedLanguageError
from modules.clicklog import info, warn, error
from modules import writer, reader
from typing import IO
import logging
import os


def parse(file: IO, language: str, opts: dict) -> None:
    """
    Parse the given file in the provided language and generate code.

    :param file: File to parse
    :param language: Programming language to use for code generation
    :param opts: Dictionary of available options
    """

    logging.debug(f'CLI: parse called with file: {file.name} and language: {language}')
    logging.debug(f'CLI: provided options: {opts}')

    try:
        fsm: dict = reader.parse_file(file)
        logging.debug(f'CLI: Parsed provided file into state machine:\n {fsm}')

        if NAME not in fsm.keys() or fsm[NAME].strip() == "":
            fsm[NAME] = 'StateMachine'

        code = process(fsm, language, opts[SKIP_VALIDATION])
        logging.debug(f'CLI: Processed state machine to code:\n{code}')

        filename = append_language_association(opts[FILENAME], language)

        if os.path.isabs(filename):
            out_path = filename

        else:
            out_path = os.path.join(opts[OUT_DIR], filename)

        try:
            logging.debug(f'CLI: Trying to save code in file: {out_path} and replace existing flag: {opts[REPLACE]}')
            writer.save_text_file(code, out_path, opts[REPLACE])
            logging.debug(f'CLI: Saved code to file')

            info(f'Saved generated code in: {out_path}')

        except ExistingFileError:
            warn(f'File: {out_path} already exists! Code could not be saved!')
            warn('Provide "-re" option to automatically overwrite existing files')

        info(f'Parsing of {file.name} finished without errors!')

    except ParsingError as pe:
        error(f'Content could not be parsed into a valid format!\n{pe.cause}')
    except ValidationError as ve:
        error(f'Validation of state machine logic failed: {ve.cause}')
    except UnsupportedLanguageError:
        error(f'Provided language: "{language}" is not supported!')
    except InternalException:
        error('Execution aborted!')
