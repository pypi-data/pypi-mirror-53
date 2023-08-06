# Other Tools for Python

Installation:

```
$ pip install othertools
```

Usage

```python
from othertools.path import chdiranchor

chdiranchor("environment.yaml", "src/.+")
```

# Examples:

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
chdiranchor("environment.yaml", "src/.+")
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
chdiranchor("environment.yaml", "src/.+")
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
