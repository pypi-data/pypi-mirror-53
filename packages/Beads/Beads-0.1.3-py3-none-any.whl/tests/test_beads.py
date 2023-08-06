#!/usr/bin/env python
import unittest
import beads.modules.reader as reader
from modules.errors import ParsingError
from io import BytesIO, TextIOWrapper


class BeadsParsingTest(unittest.TestCase):
    """
    Test class to test correct handling of .bead files
    """

    def test_correct_file_content(self):
        """
        Test that a correct file content can be parsed without error
        """
        self.maxDiff = None

        content_lines: bytes = \
            b"A:Transition_1:B\n"\
            b"A:Transition_2:C\n"\
            b"B:Transition_1:D\n"\
            b"B:Transition_3:A\n"\
            b"C:Transition_4:B"

        wrapper: TextIOWrapper = TextIOWrapper(BytesIO(content_lines))

        expected: dict = {
            'name': 'graph',
            'nodes': [
                {'id': 'A'},
                {'id': 'B'},
                {'id': 'C'},
                {'id': 'D'}
            ],
            'transitions': [
                {'label': 'Transition_1', 'from': 'A', 'to': 'B'},
                {'label': 'Transition_2', 'from': 'A', 'to': 'C'},
                {'label': 'Transition_1', 'from': 'B', 'to': 'D'},
                {'label': 'Transition_3', 'from': 'B', 'to': 'A'},
                {'label': 'Transition_4', 'from': 'C', 'to': 'B'}
            ]
        }

        actual: dict = reader.parse_beads(wrapper)

        self.assertEqual(actual, expected)

    def test_config_can_be_parsed(self):
        """
        Test that a config can be parsed without error
        """
        self.maxDiff = None

        content_lines: bytes = \
            b"#! name:GRAPH start:C\n"\
            b"A:Transition_1:B\n"\
            b"A:Transition_2:C\n"\
            b"B:Transition_1:D\n"\
            b"B:Transition_3:A\n"\
            b"C:Transition_4:B"

        wrapper: TextIOWrapper = TextIOWrapper(BytesIO(content_lines))

        expected: dict = {
            'name': 'GRAPH',
            'nodes': [
                {'id': 'A'},
                {'id': 'B'},
                {'id': 'C', "start": True},
                {'id': 'D'}
            ],
            'transitions': [
                {'label': 'Transition_1', 'from': 'A', 'to': 'B'},
                {'label': 'Transition_2', 'from': 'A', 'to': 'C'},
                {'label': 'Transition_1', 'from': 'B', 'to': 'D'},
                {'label': 'Transition_3', 'from': 'B', 'to': 'A'},
                {'label': 'Transition_4', 'from': 'C', 'to': 'B'}
            ]
        }

        actual: dict = reader.parse_beads(wrapper)

        self.assertEqual(actual, expected)

    def test_config_ignores_unsupported_values(self):
        """
        Test that a config ignores unsupported values
        """
        self.maxDiff = None

        content_lines: bytes = \
            b"#! title:GRAPH beginning:C\n"\
            b"A:Transition_1:B\n"\
            b"A:Transition_2:C\n"\
            b"B:Transition_1:D\n"\
            b"B:Transition_3:A\n"\
            b"C:Transition_4:B"

        wrapper: TextIOWrapper = TextIOWrapper(BytesIO(content_lines))

        expected: dict = {
            'name': 'graph',
            'nodes': [
                {'id': 'A'},
                {'id': 'B'},
                {'id': 'C'},
                {'id': 'D'}
            ],
            'transitions': [
                {'label': 'Transition_1', 'from': 'A', 'to': 'B'},
                {'label': 'Transition_2', 'from': 'A', 'to': 'C'},
                {'label': 'Transition_1', 'from': 'B', 'to': 'D'},
                {'label': 'Transition_3', 'from': 'B', 'to': 'A'},
                {'label': 'Transition_4', 'from': 'C', 'to': 'B'}
            ]
        }

        actual: dict = reader.parse_beads(wrapper)

        self.assertEqual(actual, expected)

    def test_parsing_handles_whitespaces_correct(self):
        """
        Test that parsing of .bead files handles whitespaces correctly
        """
        self.maxDiff = None

        content_lines: bytes = \
            b"A :Transition_1 :B\n"\
            b"A: Transition_2: C\n"\
            b"B : Transition_1 : D\n"\
            b"B   : Transition_3 :    A\n"\
            b"C: Transition_4 :B"

        wrapper: TextIOWrapper = TextIOWrapper(BytesIO(content_lines))

        expected: dict = {
            'name': 'graph',
            'nodes': [
                {'id': 'A'},
                {'id': 'B'},
                {'id': 'C'},
                {'id': 'D'}
            ],
            'transitions': [
                {'label': 'Transition_1', 'from': 'A', 'to': 'B'},
                {'label': 'Transition_2', 'from': 'A', 'to': 'C'},
                {'label': 'Transition_1', 'from': 'B', 'to': 'D'},
                {'label': 'Transition_3', 'from': 'B', 'to': 'A'},
                {'label': 'Transition_4', 'from': 'C', 'to': 'B'}
            ]
        }

        actual: dict = reader.parse_beads(wrapper)

        self.assertEqual(actual, expected)

    def test_parsing_does_not_allow_nonalpha_characters(self):
        """
        Test that parsing .bead files does not allow non alpha characters other than _
        """
        self.maxDiff = None

        content_lines: bytes = \
            b"A:Transition_1:B\n"\
            b"A:Transition_2:!C\n"\

        wrapper: TextIOWrapper = TextIOWrapper(BytesIO(content_lines))

        self.assertRaises(ParsingError, lambda: reader.parse_beads(wrapper))
