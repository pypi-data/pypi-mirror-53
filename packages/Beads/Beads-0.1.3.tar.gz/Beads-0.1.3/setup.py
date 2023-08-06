from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='Beads',
    version='0.1.3',
    author='Jakob Baatz, Rico Possienka, Pavel Nepke, Marco Wenning, Adrian Wuillemet',
    description='A commandline tool to parse fine state machines into code.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/a.wuillemet/beads',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click', 'eel', 'markdown'],
    entry_points={
        'console_scripts': [
            'beads = beads.main:beads'
        ]
    },
    keywords="state machine code generation gui",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
