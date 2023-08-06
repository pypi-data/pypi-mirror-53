#!/usr/bin/env python3
import unittest
import modules.validator as val
from modules.errors import ValidationError


class ValidationTest(unittest.TestCase):
    """
    Class to test the internal validation of state machine logic.

    Rudimentary test coverage for common cases.
    """

    def test_a_valid_machine(self):
        """
        Test that a valid machine does not raise any errors on inspection.
        """

        correct_machine: dict = {
            "name": "correct machine",
            "nodes": [
                {"id": "C"},
                {"id": "A", "start": True},
                {"id": "B"},
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "A", "label": "Transition2", "to": "C"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
            ]
        }

        val.inspect(correct_machine)

        self.assertTrue(True)

    def test_invalid_machine_with_missing_name(self):
        """
        Test that a missing name key raises a Validation error.
        """

        invalid_machine: dict = {
            # no name
            "nodes": [
                {"id": "C"},
                {"id": "A", "start": True},
                {"id": "B"},
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "A", "label": "Transition2", "to": "C"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
            ]
        }

        self.assertRaises(ValidationError, lambda: val.inspect(invalid_machine))

    def test_invalid_machine_with_missing_nodes(self):
        """
        Test that a missing nodes key raises a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            # no nodes
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "A", "label": "Transition2", "to": "C"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
            ]
        }

        self.assertRaises(ValidationError, lambda: val.inspect(invalid_machine))

    def test_invalid_machine_with_missing_transitions(self):
        """
        Test that a missing transitions key raises a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "C"},
                {"id": "A", "start": True},
                {"id": "B"},
            ]
            # no transitions
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_empty_nodes(self):
        """
        Test that no declared node raises a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                # empty nodes
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "A", "label": "Transition2", "to": "C"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_empty_transitions(self):
        """
        Test that no declared transition raises a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "C"},
                {"id": "A", "start": True},
                {"id": "B"},
            ],
            "transitions": [
                # empty transitions
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_node_missing_id(self):
        """
        Test that a node with missing id key raises a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "C"},
                {"id": "A", "start": True},
                {
                    # empty node
                },
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "A", "label": "Transition2", "to": "C"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_duplicate_nodes(self):
        """
        Test that a duplicate node declaration raises a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "C"},
                {"id": "A", "start": True},
                {
                    # duplicate id
                    "id": "C"
                },
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "A", "label": "Transition2", "to": "C"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_transitions_missing_keys(self):
        """
        Test that a duplicate node declaration raises a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "C"},
                {"id": "A", "start": True},
                {"id": "B"},
            ],
            "transitions": [
                # missing 'label'
                {"from": "A", "to": "B"},
                # missing 'to'
                {"from": "A", "label": "Transition2"},
                # missing 'from'
                {"label": "Transition1", "to": "C"},
                # missing all required keys
                {},
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_multiple_start_nodes(self):
        """
        Test that multiple start nodes raise a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "C"},
                {"id": "A", "start": True},
                # second start node
                {"id": "B", "start": True},
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "A", "label": "Transition2", "to": "C"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_unreachable_nodes(self):
        """
        Test that unreachable nodes raise a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "A", "start": True},
                {"id": "B"},
                # unreachable nodes C and D
                {"id": "C"},
                {"id": "D"}
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "B", "label": "Transition1", "to": "B"},
                {"from": "A", "label": "Transition2", "to": "A"},
                # only transition references of C and D
                {"from": "C", "label": "Transition3", "to": "D"},
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_duplicate_transitions(self):
        """
        Test that nodes that are referenced by the same transition multiple times as from node raise a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "A", "start": True},
                {"id": "B"},
                {"id": "C"},
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "B", "label": "Transition1", "to": "C"},
                # second time Transition1 references A as from node
                {"from": "A", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_undeclared_node_reference(self):
        """
        Test that a reference to an undeclared node raise a Validation error.
        """

        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "A", "start": True},
                {"id": "B"},
                {"id": "C"},
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
                # transitions that references the undeclared node D
                {"from": "A", "label": "Transition4", "to": "D"},
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)

    def test_invalid_machine_with_misspelled_node_reference(self):
        """
        Test that misspelled references to nodes raise a Validation error.
        """
        invalid_machine: dict = {
            "name": "invalid machine",
            "nodes": [
                {"id": "A", "start": True},
                {"id": "B"},
                {"id": "C"},
            ],
            "transitions": [
                {"from": "A", "label": "Transition1", "to": "B"},
                {"from": "B", "label": "Transition1", "to": "C"},
                {"from": "C", "label": "Transition3", "to": "A"},
                # transitions that references the undeclared node 'b' instead of 'B'
                {"from": "b", "label": "Transition2", "to": "A"}
            ]
        }

        with self.assertRaises(ValidationError):
            val.inspect(invalid_machine)
