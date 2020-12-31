# Enigma-Machine

[![Build Status](https://travis-ci.com/Edward-Francis/Enigma-Machine.svg?token=wYqpAnwtTqLsD1Tswm3q&branch=master)](https://travis-ci.com/Edward-Francis/Enigma-Machine)

Library for message encryption using the Enigma machine M3 and M4 variants.

## Synopsis

```python
from enigma_machine import M4

m4 = M4(
    rotors=(("I", "J", 4), ("II", "H", 9), ("III", "G", 3), ("Beta", "T", 16)),
    reflector="C-Thin",
    plugboard={"H": "I", "E": "F", "L": "M", "O": "P"},
    locked=False,
)

m4.transform_string("Hello World")  # DWVTRBGPMA
```

## Setup

```sh
# Install dependencies
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```

## Credits

This package was created with Cookiecutter and the [sourcery-ai/python-best-practices-cookiecutter](https://github.com/sourcery-ai/python-best-practices-cookiecutter) project template.
