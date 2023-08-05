# tests/conftest.py
#
# forestry: Python Tree data structures and tools
#
# Copyright (C) 2019  by Dwight D. Cummings
#
# This module is part of `forestry` and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
"""Unit tests configurations"""

# Python Standard Library imports
from collections import namedtuple
import random
from typing import Callable, Generator, Tuple
from uuid import uuid4  # for random string generation
# Third-party library imports
import pytest
# Imports for code being tested
from forestry.trees import Tree

# Helpers
Node = namedtuple('Node', 'key value')  # Key-value pairs to simulate node data
MAXINT = 100_000_000_000


# Fixtures
@pytest.fixture(scope='function')
def get_random_nodes_gen() -> Callable:
    """Return a generator emitting random node data."""

    def _get_random_nodes(n_nodes: int) -> Generator:
        for ignored in range(n_nodes):
            rand_key = str(uuid4())
            rand_value = random.randint(0, MAXINT)
            yield Node(rand_key, rand_value)

    return _get_random_nodes


@pytest.fixture(scope='function')
def get_random_nodes_list(get_random_nodes_gen) -> Callable:
    """Return a function which returns a sequence of random nodes."""

    def _get_random_nodes(n_nodes: int) -> list:
        return list(get_random_nodes_gen(n_nodes))

    return _get_random_nodes


@pytest.fixture(scope='function')
def random_node(get_random_nodes_gen) -> Node:
    """Returns a single random node."""
    return next(get_random_nodes_gen(1))


@pytest.fixture(scope='function')
def single_node_tree(random_node) -> Tuple[Tree, Node]:
    """Return tree with a single node and its key value pair"""
    t = Tree(key=random_node.key, value=random_node.value)
    return t, random_node


@pytest.fixture(scope='function')
def two_level_tree(get_random_nodes_list) -> Tuple[Tree, list]:
    """Return a random two level tree"""
    random_nodes = get_random_nodes_list(random.randint(2, 100))
    first_node, second_node, *rest_nodes = random_nodes
    t = Tree(key=first_node.key, value=first_node.value)
    t.append(key=second_node.key, value=second_node.value)
    t.extend(children=rest_nodes, parent=first_node.key)

    return t, random_nodes
