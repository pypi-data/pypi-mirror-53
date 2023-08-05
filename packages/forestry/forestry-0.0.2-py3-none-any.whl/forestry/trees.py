# forestry/trees.py
#
# forestry: Python Tree data structures and tools
#
# Copyright (C) 2019  by Dwight D. Cummings
#
# This module is part of `forestry` and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
"""Provides a Tree class for building tree data structures"""

# Standard library imports
from collections import defaultdict, deque, OrderedDict
from typing import (
    Any, NamedTuple, Union, Iterable, Tuple, Generator
)

# Global variables
EMPTY = object()  # Sentinel Value


# Classes
class _Node(NamedTuple):
    """Encapsulates Tree node data.

    An internal helper class supporting Tree class definition
    """
    value: Any  # The data stored at the node
    level: int = 1  # The depth level of the node in the tree
    parent: Union[str, object] = EMPTY  # The key of parent


class _TreeInfo(NamedTuple):
    """Provide names for tree info attributes.

    Returned by the Tree.info() function.
    """
    root: Union[Tuple, object]  # Key-value of root node or EMPTY
    size: int  # size or len of tree
    n_leaves: int  # number of leaves
    degree: int  # number of children of root node
    height: int  # maximum level of any node in the tree


_TreeInfo.__name__ = 'TreeInfo'


class Tree:
    """Used to create and query Tree data structures.

    Trees are hierarchical collections of nodes. Trees
    are build starting from a root node. Each node stores
    arbitrary data, its "value", and a label, name
    or node identifier, called a "tag".

    Values in the tree can be accessed by looking up the
    nodes' tags.

    Examples:
        >>> from forestry import Tree
        >>> t = Tree(key='a', value=1)
        >>> assert t['a'] == 1
        >>> t.append(key='b', value=2)  # Adds a child to the root node by default
        >>> assert t['b'] == 2
        >>> t.append(key='c', value=3)  # Add another child to the root node
        >>> t.parent(key='c') == 1  # Ask for the parent of c
        >>> t.children(key='a') == [2, 3]  # Ask for the children of a
        >>> t.append(key='d', value=4, parent='b')  # Adds child to b
        >>> assert t.ancestors(key='d') == [2, 1]
        >>> assert t.path(key='d') == [1, 2, 4]  # Traverse from root to node

    Attributes:
        root_key (str): key of root node
        root_value (Any): value of root node
    """
    __slots__ = ['_children', '_nodes', 'root_key']

    def __init__(self,
                 key: Union[str, object] = EMPTY,
                 value: Any = EMPTY) -> None:
        """This method initializes instance variables.

        Args:
            key (Union[str, object]): tag or name of the node
            value (Any): The data value stored at the node.
        """
        self._children = defaultdict(list)
        self._nodes = OrderedDict()
        if value is not EMPTY and key is not EMPTY:
            self._nodes[key] = _Node(value)

        self.root_key = key

    def __contains__(self, item) -> bool:
        return item in self._nodes

    def __getitem__(self, item) -> Any:
        return self._nodes[item].value

    def __len__(self) -> int:
        return len(self._nodes)

    def __repr__(self):
        """<Tree; root=('abc', 1); size=9>"""
        cls_name = type(self).__name__
        if self.is_empty():
            return f'<{cls_name}; root=EMPTY; size=0>'
        return (
            f'<{cls_name}; root=({self.root_key!r}, {self.root_value!r}); '
            f'size={len(self)}>'
        )

    @property
    def root_value(self) -> Union[Any, object]:
        """Return the value stored at root"""
        return self[self.root_key]

    def ancestors(self, key: str, reverse: bool = False) -> list:
        """Returns a list of parent and recursive parents.

        Args:
            key (str): the key whose ancestors are returned
            reverse (bool): build ancestry from the root down
        """
        self._verify_present(key)
        deq = deque()
        current_key = key
        while not self.is_root(current_key):
            current_key = self._nodes[current_key].parent
            add_to_deq = deq.appendleft if reverse else deq.append
            add_to_deq(self[current_key])

        return list(deq)

    def append(self, key: str, value: Any,
               parent: str = EMPTY) -> None:
        """Adds a child node to the root node.

        Args:
            key (str): tag or name of the node
            value (Any): The data value stored at the node.
            parent (str): The parent to append the child to
        """
        if self.is_empty() and parent is not EMPTY:
            msg = 'Cannot append to parent node in empty tree'
            raise ValueError(msg)

        if self.is_empty():
            self._nodes[key] = _Node(value)
            self.root_key = key
            return

        parent = parent if parent is not EMPTY else self.root_key
        self._verify_absent(key)
        self._verify_present(parent)
        level = self.level(parent) + 1
        self._nodes[key] = _Node(value, level, parent)
        self._children[parent].append(key)

    def children(self, key: str) -> list:
        """Return the list of child nodes.

        Args:
            key (str): key of node whose children are returned.
        """
        self._verify_present(key)
        return [self[child_key] for child_key in self._children[key]]

    def extend(self, children: Iterable[Tuple[str, Any]],
               parent: str = None) -> None:
        """Adds child nodes to a parent.

        Args:
            children (Iterable[Tuple[str, Any]]): Iterable of key-value pairs
            parent (str): The parent to append the children to
        """
        for key, value in children:
            self.append(key, value, parent)

    def display(self):
        """Present a hierarchical display of the tree"""
        print()
        print(self.info())
        for value, level in self.preorder(levels=True):
            if level == 1:
                print(repr(value))
                continue

            print('\t' * (level - 1) + '|__ ' + repr(value))

    def info(self):
        """Return a named tuple of tree information"""
        if self.is_empty():
            return _TreeInfo(
                root=EMPTY,
                size=0,
                n_leaves=0,
                degree=0,
                height=0
            )

        return _TreeInfo(
            root=(self.root_key, self.root_value),
            size=len(self),
            n_leaves=len(self.leaves()),
            degree=len(self.children(key=self.root_key)),
            height=max(n.level for n in self._nodes.values())
        )

    def is_empty(self) -> bool:
        """True if tree is empty, else false."""
        return self.root_key is EMPTY

    def is_leaf(self, key: str) -> bool:
        """True if tree is empty, else false.

        Args:
            key (str): key of node being checked."""
        self._verify_present(key)
        return self.children(key=key) == []

    def is_root(self, key: str) -> bool:
        """Returns true if given key is root_key

        Args:
            key (str): key of node being checked."""
        self._verify_present(key)
        return key == self.root_key

    def leaves(self) -> list:
        """Return values of those nodes that have no children."""
        return [
            self[key] for key in self._nodes
            if self._children[key] == []
        ]

    leafs = leaves

    def level(self, key: str) -> int:
        """Return 1 + the number of edges between a node and the root.

        Args:
            key (str): the key whose level is being returned
        """
        return self._nodes[key].level

    def level_nodes(self, level: int) -> list:
        """Return all the node values at a given level.

        Args:
            level (int): the level whose nodes are being returned
        """
        return [
            node.value
            for node in self._nodes.values()
            if node.level == level
        ]

    def parent(self, key: str) -> Any:
        """Return the value of the parent node.

        Args:
            key (str): the key whose parent is returned
        """
        parent_key = self._nodes[key].parent
        if parent_key is EMPTY:
            return EMPTY
        return self._nodes[parent_key].value

    def path(self, key: str) -> list:
        """Returns ancestry from root to node at `key` including
        the give node.

        Args:
            key (str): the key whose ancestors are returned
        """
        # The call to `ancestors` check for key errors.
        return self.ancestors(key, reverse=True) + [self[key]]

    def preorder(self,
                 start_key: str = None,
                 levels: bool = False,
                 verify_start_key: bool = False) -> Generator:
        """Return an iterable of nodes in 'pre-order'

        Args:
            start_key (str): key of node to start traversal.
            levels (bool): if true, return each nodes value and level
            verify_start_key (bool): if true, raises key error for bad key
                else returns an empty iterable.
        """
        yield from self._traverse('preorder', start_key, levels, verify_start_key)

    def postorder(self,
                  start_key: str = None,
                  levels: bool = False,
                  verify_start_key: bool = False) -> Generator:
        """Return an iterable of nodes in 'post-order'

        Args:
            start_key (str): key of node to start traversal.
            levels (bool): if true, return each nodes value and level
            verify_start_key (bool): if true, raises key error for bad key
                else returns an empty iterable.
        """
        yield from self._traverse('postorder', start_key, levels, verify_start_key)

    def inorder(self,
                start_key: str = None,
                levels: bool = False,
                verify_start_key: bool = False) -> Generator:
        """Return an iterable of nodes in 'in-order'

        Args:
            start_key (str): key of node to start traversal.
            levels (bool): if true, return each nodes value and level
            verify_start_key (bool): if true, raises key error for bad key
                else returns an empty iterable.
        """
        yield from self._traverse('inorder', start_key, levels, verify_start_key)

    def levelorder(self,
                   start_key: str = None,
                   levels: bool = False,
                   verify_start_key: bool = False) -> Generator:
        """Return an iterable of nodes in 'level-order'

        Args:
            start_key (str): key of node to start traversal.
            levels (bool): if true, return each nodes value and level
            verify_start_key (bool): if true, raises key error for bad key
                else returns an empty iterable.
        """
        yield from self._traverse('levelorder', start_key, levels, verify_start_key)

    def siblings(self, key: str) -> list:
        """Return the list of child nodes of parent."""
        self._verify_present(key)
        if key == self.root_key:
            return []
        siblings = self._children[self._nodes[key].parent]
        return [self[k] for k in siblings if k != key]

    ##
    # Helpers
    ##
    def _preorder(self, start_key) -> Generator:
        """Helper function visits each node in "preorder".

        Args:
            start_key (str): the key of the node to start the traversal
        """
        yield start_key
        for child in self._children[start_key]:
            yield from self._preorder(start_key=child)

    def _postorder(self, start_key) -> Generator:
        """Helper which visits each node in "postorder".

        Args:
            start_key (str): the key of the node to start the traversal
        """
        for child in self._children[start_key]:
            yield from self._postorder(start_key=child)
        yield start_key

    def _inorder(self, start_key) -> Generator:
        """Helper which visits each node in "inorder" and call the visit
        function.

        Args:
            start_key (str): the key of the node to start the traversal
        """
        first = self._children[start_key][0:1]
        rest = self._children[start_key][1:]
        if first:
            yield from self._inorder(start_key=first[0])

        yield start_key
        for child in rest:
            yield from self._inorder(start_key=child)

    def _levelorder(self, start_key) -> Generator:
        """Helper which visits each node in "levelorder".

        Args:
            start_key (str): the key of the node to start the traversal
        """
        deq = deque([start_key])
        while deq:
            key = deq.popleft()
            yield key
            deq.extend(self._children[key])

    def _traverse(self, order: str,
                  start_key: str = None,
                  levels: bool = False,
                  verify_start_key: bool = False) -> Generator:
        """Helper function to traverse the tree in given order"""
        start_key = start_key or self.root_key
        if verify_start_key:
            self._verify_present(start_key)

        if start_key not in self:
            return

        traverse_order = getattr(self, '_' + order)
        for key in traverse_order(start_key):
            if levels:
                yield (self[key], self.level(key))
            else:
                yield self[key]

    def _verify_present(self, key: str) -> None:
        """Raise KeyError if key missing.
        Args:
            key (str): the key to verify
        """
        if key not in self:
            raise KeyError(f'Key "{key}" was never added')

    def _verify_absent(self, key: str) -> None:
        """Raise KeyError if key present.
        Args:
            key (str): the key to verify
        """
        if key in self:
            raise KeyError(f'Key "{key}" already added')
