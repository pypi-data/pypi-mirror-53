# tests/test_trees.py
#
# forestry: Python Tree data structures and tools
#
# Copyright (C) 2019  by Dwight D. Cummings
#
# This module is part of `forestry` and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
"""Unit tests for module trees.py"""

# Third-party library imports
import pytest
# Imports for code being tested
from forestry.trees import Tree, EMPTY


##
# Unit Tests
##
def test_empty_tree(random_node):
    empty_tree = Tree()
    print(empty_tree)
    # empty tests
    assert empty_tree.is_empty() and len(empty_tree) == 0
    # key lookup failure
    with pytest.raises(KeyError):
        ignored = empty_tree[random_node.key]

    # Key errors on methods lookup methods
    for name in ['ancestors', 'children', 'level', 'parent', 'path',
                 'siblings']:
        method = getattr(empty_tree, name)
        with pytest.raises(KeyError):
            ignored = method(random_node.key)
    # Empty list return for method returning sequences or iterables
    for name in ['leaves', 'inorder', 'postorder', 'preorder',
                 'levelorder']:
        method = getattr(empty_tree, name)
        assert list(method()) == []
    assert (
            empty_tree.level_nodes(level=1) == []
            and empty_tree.info().size == 0
            and empty_tree.info().n_leaves == 0
            and empty_tree.info().degree == 0
            and empty_tree.info().height == 0
    )
    # Test adding to empty tree
    with pytest.raises(ValueError):
        empty_tree.append('foo', 1, parent='bar')

    empty_tree.append('foo', 1)
    print(empty_tree)



def test_single_node_tree(single_node_tree):
    t, node = single_node_tree
    print(t)
    # try appending a duplicate key
    with pytest.raises(KeyError):
        t.append(key=t.root_key, value='foo')

    assert (
            t.root_key == node.key
            and t.root_value == t[node.key] == node.value
            and node.key in t
            and t.is_leaf(key=node.key)
            and t.is_root(key=node.key)
            and not t.is_empty()
            and t.level(key=node.key) == 1
            and t.parent(key=node.key) is EMPTY
            and t.children(key=node.key) == []
            and t.siblings(key=node.key) == []
            and t.ancestors(key=node.key) == []
            and t.path(key=node.key) == [node.value]
            and t.leaves() == [node.value]
            and len(t) == 1
            and list(t.inorder()) == [node.value]
            and list(t.postorder()) == [node.value]
            and list(t.preorder()) == [node.value]
            and list(t.levelorder()) == [node.value]
            and t.level_nodes(level=1) == [node.value]
            and t.level_nodes(level=999) == []
            and t.info().size == 1
            and t.info().n_leaves == 1
            and t.info().degree == 0
            and t.info().height == 1
    )


def test_two_level_tree(two_level_tree):
    t, nodes = two_level_tree
    t.display()
    first_node, *rest_nodes = nodes
    assert (
            t.root_key == first_node.key
            and t.root_value == t[first_node.key] == first_node.value
            and all(n.key in t for n in nodes)
            and all(t.is_leaf(key=n.key) for n in rest_nodes)
            and all(not t.is_root(key=n.key) for n in rest_nodes)
            and t.is_root(key=first_node.key)
            and not t.is_empty()
            and t.level(key=first_node.key) == 1
            and all(t.level(key=n.key) == 2 for n in rest_nodes)
            and t.level_nodes(level=1) == [first_node.value]
            and t.level_nodes(level=2) == [n.value for n in rest_nodes]
            and t.parent(key=first_node.key) is EMPTY
            and all(t.parent(key=n.key) is first_node.value for n in rest_nodes)
            and t.children(key=first_node.key) == t.level_nodes(level=2)
            and all(t.parent(key=n.key) == first_node.value for n in rest_nodes)
            and all(t.siblings(key=n.key) ==
                    [n2.value for n2 in rest_nodes if n2 != n]
                    for n in rest_nodes
                    )
            and t.ancestors(key=first_node.key) == []
            and all(t.ancestors(key=n.key) == [first_node.value] for n in rest_nodes)
            and t.path(key=first_node.key) == [first_node.value]
            and all(t.path(key=n.key) == [first_node.value, n.value]
                    for n in rest_nodes
                    )
            and t.leaves() == [n.value for n in rest_nodes]
            and len(t) == len(nodes)
            and list(t.inorder()) == [
                rest_nodes[0].value, first_node.value,
                *[n.value for n in rest_nodes[1:]]
            ]
            and list(t.postorder()) == [
                *[n.value for n in rest_nodes],
                first_node.value
            ]
            and list(t.preorder()) == [n.value for n in nodes]
            and list(t.preorder(start_key=t.root_key,
                                verify_start_key=True))
            == [n.value for n in nodes]
            and list(t.levelorder()) == [n.value for n in nodes]
            and t.level_nodes(level=1) == [first_node.value]
            and t.level_nodes(level=2) == [n.value for n in rest_nodes]
            and t.level_nodes(level=-999) == []
            and t.info().size == len(nodes)
            and t.info().n_leaves == len(rest_nodes)
            and t.info().degree == len(rest_nodes)
            and t.info().height == 2
    )
