from meta import *
from modules.errors import ValidationError
from modules.generator import group_transitions
import logging


def inspect(fsm: dict) -> None:
    """
    Inspect the provided fsm and assert the correctness of its internal logic.

    Provide a dictionary that represents a fine state machine as:

        {
            name: "",
            nodes: [
                {id: , ...}
            ],
            transitions: [
                {label: , from: , to: , ...}
            ]
        }

    All above displayed keys are required to pass validation. Other keys are optional and allowed.

    :param fsm: Fine state machine parsed as dictionary.
    :return: True if every assertion is true
    :raises ValidationError on any invalid logic
    """
    try:
        # assert fsm contains necessary keys
        keys = fsm.keys()

        assert NAME in keys, f'Missing required key: {NAME}'
        assert NODES in keys, f'Missing required key: {NODES}!'
        assert TRANSITIONS in keys, f'Missing required key: {TRANSITIONS}!'

        # assert fsm contains at least one node
        nodes: list = fsm[NODES]
        assert len(nodes) > 0, 'No state is defined!'

        # assert fsm contains at least one transition
        transitions: list = fsm[TRANSITIONS]
        assert len(transitions) > 0, 'No transition is defined!'

        # assert all nodes have the required 'id' key
        faulty_nodes = nodes_with_no_id(nodes)
        assert len(faulty_nodes) == 0, f'{len(faulty_nodes)} node(s) are missing the required key "{ID}"'

        # assert id of nodes is unique
        duplicate_nodes: list = duplicated_nodes(nodes)
        assert len(duplicate_nodes) == 0, f'These node(s) have been declared more than once: {duplicate_nodes}'

        # assert all transitions have the required keys 'label', 'from', 'to'
        faulty_transitions: list = transitions_with_missing_keys(transitions)
        assert len(faulty_transitions) == 0, f'Required keys [{LABEL},{FROM},{TO}] missing' \
            f' in transitions: {faulty_transitions}'

        # assert maximum of one start node
        start_nodes, start_node = identify_start_nodes(nodes)
        assert len(start_nodes) < 2, f'More than one start state: {start_nodes}'

        transitions_grouped_by_from: dict = group_transitions(transitions, group_by=FROM)
        start_node = start_node if start_node is not None else next(iter(nodes))[ID]

        # assert that all nodes are reachable
        isolated_nodes: set = unreachable_nodes(nodes, transitions_grouped_by_from, start_node)
        assert len(isolated_nodes) == 0, f'Not all nodes can be reached: {isolated_nodes}'

        transitions_grouped_by_label: dict = group_transitions(transitions, group_by=LABEL)

        # assert that for each transition label a from node exists only once
        conflicting_transition_list: list = conflicting_transitions(transitions_grouped_by_label)
        assert len(conflicting_transition_list) == 0, f'Conflicting transitions for: {conflicting_transition_list}'

        # assert all nodes referenced in transitions are declared
        undeclared_nodes: set = inspect_transitions_for_undeclared_nodes(nodes, transitions)
        assert len(undeclared_nodes) == 0, f'States referenced but not declared: {undeclared_nodes}'

    except AssertionError as ae:
        logging.debug('VALIDATION: Failed due to AssertionError')
        raise ValidationError(ae)


def unreachable_nodes(nodes: list, grouped_transitions: dict, start_node: str) -> set:
    """
    Transition over the NODES starting with the initial START_NODE via the GROUPED_TRANISIONS and return any node that
    was not visited in the process.

    :param nodes: List of all nodes
    :param grouped_transitions: Dictionary of all transitions grouped by their FROM node
    :param start_node: Node to start from
    :return: List of nodes in NODES that were not visited
    """

    isolated_nodes: set = set(node[ID] for node in nodes)
    isolated_nodes.discard(start_node)

    node_queue: list = [start_node]

    while len(node_queue) > 0:
        node: str = node_queue.pop(0)

        if node in grouped_transitions.keys():
            associated_transitions: list = grouped_transitions[node]

            for to_node in associated_transitions:
                if isolated_nodes.__contains__(to_node[node]):
                    isolated_nodes.discard(to_node[node])
                    node_queue.append(to_node[node])

    return isolated_nodes


def conflicting_transitions(transitions_grouped_by_label: dict) -> list:
    """
    Group all labels of TRANSITIONS that are declared multiple times from the same state.

    :param transitions_grouped_by_label: All Transitions grouped by their label
    :return: List of labels of conflicting transitions
    """

    conflicting_transitions_list: list = []

    for label, transitions_for_label in transitions_grouped_by_label.items():
        unique_ids = set(next(iter(t)) for t in transitions_for_label)

        if len(unique_ids) != len(transitions_for_label):
            conflicting_transitions_list.append(label)

    return conflicting_transitions_list


def identify_start_nodes(nodes: list) -> (list, str or None):
    """
    List all node ids of nodes that are declared as start nodes.

    :param nodes: All nodes
    :return: List of nodes declared as start, the last found start node or None if none was found
    """
    start_nodes: list = []
    start_node: str or None = None

    for node in nodes:
        if START in node.keys() and node[START] is True:
            start_nodes.append(node[ID])
            start_node = node[ID]

    return start_nodes, start_node


def duplicated_nodes(nodes: list) -> list:
    """
    List all nodes that have been declared more than once.

    :param nodes: All nodes
    :return: List of duplicated node ids
    """

    duplicate_nodes: list = []
    found_nodes: set = set()

    for node in nodes:
        node_id = node[ID]
        if node_id in found_nodes:
            duplicate_nodes.append(node_id)
        else:
            found_nodes.add(node_id)

    return duplicate_nodes


def nodes_with_no_id(nodes: list) -> list:
    """
    List of all nodes without ID key

    :param nodes: All nodes
    :return: List of nodes without ID key
    """
    faulty_nodes: list = []

    for node in nodes:
        if ID not in node.keys():
            faulty_nodes.append(node)

    return faulty_nodes


def transitions_with_missing_keys(transitions: list) -> list:
    """
    List transitions that miss at least one of the required keys:
        'label', 'from', 'to'

    :param transitions: All transitions
    :return: List of transitions missing a required key
    """

    faulty_transitions: list = []

    for transition in transitions:
        if {LABEL, FROM, TO} > transition.keys():
            faulty_transitions.append(transition)

    return faulty_transitions


def inspect_transitions_for_undeclared_nodes(nodes: list, transitions: list) -> set:
    """
    List all nodes that have been referenced in a transition but haven't been declared.

    :param nodes: All nodes
    :param transitions: All transitions
    :return: List of node ids that are referenced but not declared
    """
    declared_nodes: set = set(node[ID] for node in nodes)
    undeclared_nodes: set = set()

    for transition in transitions:
        _from = transition[FROM]
        _to = transition[TO]

        if _from not in declared_nodes:
            undeclared_nodes.add(_from)

        if _to not in declared_nodes:
            undeclared_nodes.add(_to)

    return undeclared_nodes
