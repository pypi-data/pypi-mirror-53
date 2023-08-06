# Other Tools for Python

# To Publish

```
$ python setup.py sdist
$ twine upload dist/othertools-X.X.X.tar.gz
```

# Installation

```
$ pip install othertools

# other useful commands
$ pip show othertools | findstr "Version"
$ pip install othertools --upgrade
```

## Usage

```python
from othertools.path import chdir_by_anchor
chdir_by_anchor("environment.yaml", "src/.+")
#---
from othertools.path import path_add_by_anchor
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
