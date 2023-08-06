# Syllogio Identify Propositions

Identify natural language propositions in a written argument.

# Installation

1. Install pip package.

   ```bash
   pip install syllogio-identifyPropositions
   ```

2. Install [spacy module](https://spacy.io/models) (Tested with "en_core_web_sm").

   ```
   python -m spacy download <model name>
   ```

3. Add model name to configuration.

   ```ini
   ; setup.cfg

   [syllogio-identifyPropositions]
   model_name = <model name> ; defaults to "en_core_web_sm"
   ```

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
