import click


def info(text: str) -> None:
    """
    Convenience click.echo call with '[INFO]: ' prefix

    :param text: String to log on terminal
    """
    click.echo(f'[INFO]: {text}')


def warn(text: str) -> None:
    """
    Convenience click.secho with fg=yellow.

    Text will be prefixed with '[WARN]: ' and printed in yellow.

    :param text: String to log on terminal
    """
    click.secho(f'[WARN]: {text}', fg='yellow')


def error(text: str) -> None:
    """
    Convenience click.secho with fg=red.

    Text will be prefixed with '[ERROR]: ' and printed in red.

    :param text: String to log on terminal
    """
    click.secho(f'[ERROR]: {text}', fg='red')


class Overview:
    """
    Overview to print on CommandLine.

    Provide the title of the overview on initialization.
    """

    def __init__(self, title: str):
        self.title = title

    def print(self, info) -> None:
        """
        Print the Overview on the CommandLine with it title and the given INFO in its body.

        :param info: Generator for strings to print as overviews body
        """
        click.echo(f'[OVERVIEW]: {self.title}:')
        click.echo('|')
        for item in info:
            click.echo(f'| {item}')
        click.echo('|')
