# Syllogio Identify Propositions

Identify natural language propositions in a written argument.

# Installation

`pip install syllogio-identifyPropositions`

# Usage

Command line

```
> idpr "All men are mortal. Socrates is a man. Therefore, Socrates is mortal."
[
  "All men are mortal",
  "Socrates is a man",
  "Therefore, Socrates is mortal"
]
```

Programmatic

```python
from identifyPropositions import identify

propositions = identify("All men are mortal. Socrates is a man. Therefore, Socrates is mortal.")

# propositions will be:
# [
#   "All men are mortal",
#   "Socrates is a man",
#   "Therefore, Socrates is mortal"
# ]
```
