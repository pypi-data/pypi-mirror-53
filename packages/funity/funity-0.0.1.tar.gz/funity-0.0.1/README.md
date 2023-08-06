# funity

A Unity3d installation finder and command line helper.

## Installation

```sh
pip install funity
```

## Usage

### In Terminal

```sh
python -m funity

# Outputs a JSON-formatted file containing all Unity3d editors found in the current working directory.

# editor.cache
# [
#   "/Applications/Unity/Hub/Editor/2019.2.6f1"
# ]
```

### In Python

```python
from funity import *


editors = UnityEditor.find_all()

editor = editors[0]

project = UnityProject('/Users/you/Projects/HelloWorld')

return_code = editor.run(
    '-projectPath', str(project),
    '-buildTarget', 'Win64',
    '-executeMethod', 'BuildPlayerCommand.Execute',
    cli=True,  # Shorthand for '-batchmode', '-nographics', '-quit', '-silent-crashes'.
    log_func=lambda l: print(l, end='')  # Prints all logs from Unity.
)
```