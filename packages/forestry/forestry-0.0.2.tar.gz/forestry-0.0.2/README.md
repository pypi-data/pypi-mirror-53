# Forestry
Python Tree data structures and tools.

# Forestry Package Installation
Install `forestry` with python's `pipenv` or `pip` package managers.
```console
$ pipenv install forestry
```
```console
$ pip install forestry
```

# Getting Started
```
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
``` 

