from meta import *
from string import Template
import logging


class CodeGenerator:
    """
    Class handling the build process of code based on a fine state machine representation.

    Requires a language template on initialization to be provided to the constructor.
    For template definition and examples see: resources/templates/template

    Constructed code follows a predefined schema:

            1. A variable/collection/class/enum holding all possible states

            2. A variable holding the current state

            3. Methods that represent transition rules upon certain events
    """

    def __init__(self, template: dict):
        self.template: dict = template
        self.config: dict = template[CONFIG]
        self.states: dict = template[STATES]
        self.state: dict = template[STATE]
        self.transitions: dict = template[TRANSITIONS]
        self.header: dict = template[HEADER]
        self.footer: dict = template[FOOTER]

    def build(self, fsm: dict) -> str:
        """
        Build code from a parsed fsm representation.

        Method will assume that the given representation is correct and perform
        no further validation.

        :param fsm: Parsed dictionary representation of a fine state machine
        :return: code corresponding to the fsm
        """

        all_nodes: list = sorted(fsm[NODES], key=lambda node: node[ID])

        states_code = self.write_all_states(all_nodes)
        logging.debug(f'GENERATOR: Generated code for all states:\n{states_code}')

        first_state: str = next(iter(all_nodes))[ID]
        state_code = self.write_initial_state(all_nodes, first_state)
        logging.debug(f'GENERATOR: Generated states variable:\n{state_code}')

        transitions: dict = group_transitions(fsm[TRANSITIONS])
        functions_code = self.write_all_functions(transitions)
        logging.debug(f'GENERATOR: Generated transition code:\n{functions_code}')

        code_blocks: list = [
            states_code,
            state_code,
            functions_code
        ]

        if self.config[USE_HEADER]:
            header = self.write_header(self.header[CONTENT], fsm[NAME])
            code_blocks.insert(0, header)

            footer = self.write_footer(self.footer[CONTENT])
            code_blocks.append(footer)

        return self.config[GAP].join(code_blocks)

    def write_header(self, header_template: Template, name: str) -> str:
        return self.substitute(header_template, name=name)

    def write_footer(self, footer_template: Template) -> str:
        return self.substitute(footer_template)

    def write_all_states(self, nodes: list) -> str:
        """
        Build code that represents all states contained in the fsm.

        All found nodes will be represented in a distinct state. All states will be added to one
        global variable (class/enum/var or equivalent).

        :param nodes: List of all nodes
        :return: Code corresponding to a state collection
        """

        item_template: Template = self.states[ITEM]
        body_template: Template = self.states[BODY]

        items: str = ''
        for index, node in enumerate(nodes):
            name: str = node[ID]
            item: str = self.substitute(item_template, name=name, value=f'{index}')

            items = ''.join([items, item])

        return self.substitute(body_template, items=items)

    def write_initial_state(self, nodes: list, backup_initial: str) -> str:
        """
        Write code that assigns an initial state to a variable.

        The variable from this code snippet will be used throughout to represent the current state.
        Provide a backup value for the initial state that will be used if no node declaring itself as initial state
        can be found.

        :param nodes: List of all nodes
        :param backup_initial: Initial state value to use if no initial node is detected
        :return: Code that handles the initial state assignment
        """

        body_template: Template = self.state[BODY]

        initial_state: str = backup_initial
        for node in nodes:
            if START in node.keys() and node[START]:
                initial_state = node[ID]
                break

        return self.substitute(body_template, value=initial_state)

    def write_all_functions(self, transitions: dict) -> str:
        """
        Write the event handling code responsible for transition between states.

        Methods needs provision of all transitions grouped by their label.

        :param transitions: Dictionary of all transitions grouped by their label
        :return: Code handling transitions between states
        """

        functions_code: list = []
        for name, assignments in sorted(transitions.items(), key=lambda item: item[0]):

            sorted_assignments = sorted(assignments, key=lambda assignment: next(iter(assignment)))

            functions_code.append(self.write_function(name, sorted_assignments))

        return self.config[GAP].join(functions_code)

    def write_function(self, name: str, assignments: list):
        """
        Write code that represents all transitions that can happen for one distinct event.

        :param name: Name of the event / transition
        :param assignments: Dictionary of all transitions for the event
        :return: Code of one method/function as transition rules
        """

        body_template: Template = self.transitions[BODY]
        item_template: Template = self.transitions[ITEM]

        items = ''

        # Handle a differing first assignment as in 'if ... elif'
        if len(assignments) > 0 and ITEM_FIRST in self.transitions.keys():
            first_item_template: Template = self.transitions[ITEM_FIRST]
            first_assignment: dict = assignments.pop(0)

            for _from, _to in first_assignment.items():
                items = self.substitute(first_item_template, name=_from, value=_to)

        for assignment in assignments:
            for _from, _to in assignment.items():
                item = self.substitute(item_template, name=_from, value=_to)
                items = ''.join([items, item])

        return self.substitute(body_template, name=name, items=items)

    def substitute(self, template: Template, name: str = None, value: str = None, items: str = None) -> str:
        """
        Internal method handling Template.safe_substitute while always providing three fixed variables:

                $indent, $state, $states placeholders of all provided TEMPLATES will be substituted.

        In addition provide name / value / items as non fixed parameters.

        :param template: String template to substitute values in
        :param name: Value for '$name' placeholder in template
        :param value: Value for '$value' placeholder in template
        :param items: Value for '$items' placeholder in template
        :return: Template substitution
        """
        indent = self.config[INDENT]
        state = self.state[NAME]
        states = self.states[NAME]

        return template.safe_substitute(indent=indent, state=state, states=states, name=name, value=value, items=items)


def group_transitions(transitions: list, group_by: str = LABEL) -> dict:
    """
    Group transitions by their label.

    Transitions need to at have the following keys:
        'label': descriptive id of transition
        'from': Start Node
        'to': End Node

    :param transitions: All transitions
    :param group_by: The key to group by, defaults to 'label'
    :return: Transitions grouped by key
    """

    grouped_transitions = dict()

    for transition in transitions:
        label = transition[group_by]
        trans = {transition[FROM]: transition[TO]}

        if label not in grouped_transitions.keys():
            grouped_transitions[label] = [trans]
        else:
            grouped_transitions[label].append(trans)

    logging.debug(f'GENERATOR: Grouped transitions to:\n{grouped_transitions}')
    return grouped_transitions
