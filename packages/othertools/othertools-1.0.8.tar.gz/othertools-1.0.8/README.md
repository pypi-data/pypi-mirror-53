# Other Tools for Python

# To Publish

```
$ python setup.py sdist
$ twine upload dist/*
```

# Installation

```
$ pip install othertools
```

## Usage

```python
from othertools.path import chdir_by_anchor
from othertools.path import path_add_by_anchor

chdir_by_anchor("environment.yaml", "src/.+")
path_add_by_anchor("environment.yaml", "src/.+")
```

# Examples

## Example 1

Before:
```
.
├── documents
└── projects
    └── python
        └── hello-world
            ├── environment.yaml
            └── src ### CURRENT DIRECTORY] ###
                └── root.package
                    └── main.py
```

```python
chdir_by_anchor("environment.yaml", "src/.+")
```

After:
```
.
├── documents
└── projects
    └── python
        └── hello-world
            ├── environment.yaml
            └── src
                └── root.package ### CURRENT DIRECTORY] ###
                    └── main.py
```

## Example 2

Before:
```
.
├── documents
└── projects
    └── python
        └── hello-world ### CURRENT DIRECTORY] ###
            ├── environment.yaml
            └── src
                └── root.package
                    └── main.py
```

```python
chdir_by_anchor("environment.yaml", "src/.+")
```

After:
```
.
├── documents
└── projects
    └── python
        └── hello-world
            ├── environment.yaml
            └── src
                └── root.package ### CURRENT DIRECTORY] ###
                    └── main.py
```
