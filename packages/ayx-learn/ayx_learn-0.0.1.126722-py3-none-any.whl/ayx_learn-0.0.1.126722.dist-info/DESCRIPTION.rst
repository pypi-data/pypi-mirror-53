[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# ayx-learn

A foundation of [scikit-learn](https://scikit-learn.org/stable/) compatible data science tools, such as Transformers, that both Alteryx Assisted Modeling and Code Fee Tools are built on.

## Source code organization

```
.
├── README.md
├── ayx_learn: Source code for the ayx_learn package.
│   ├── cmd: CLI commands that enable transformers and other functions to be used directly from the command-line.
│   ├── transformers: Transformer source code.
│   └── utils: Utility functions, such as validation.
├── docs: Sphinx documentation.
├── examples: CLI examples that use ayx_learn/cmd and DVC.
├── notebooks: Jupyter notebooks.
├── requirements-dev.txt: Requirements for development env.
├── requirements.txt: Requirements for building and running in a production env.
├── setup.py
├── tests
│   └── unit: pytest unit tests.
└── tox.ini: Ini file for tox.
```

## Code standards

`ayx-learn` follows the [Alteryx Python Code Standards](https://alteryx.quip.com/qR3kAG4OA32X/Python-Code-Standards)

## Error handling and Logging

Errors/exceptions in `ayx-learn` follow the `Message and Raise` and `Transformer` patterns described in the blog at [Exceptional logging of exceptions in Python](https://www.loggly.com/blog/exceptional-logging-of-exceptions-in-python/).

Following the recommendations at, [Configuring Logging for a Library](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library), a NullHandler has been initialized at `ayx_learn` module scope.
Clients of `ayx-learn` can easily provide a logging handler that will override the NullHandler by initializing a handler in the client.
E.g.

```
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
```

## Testing

Unit tests are written using [pytest](https://docs.pytest.org/) and are located in `./tests/unit`.

[tox](https://tox.readthedocs.io/) can be used for creating a virtualenv and automatically running the pytest unit tests.

## Examples

A set of CLI examples based on ayx_learn/cmd that use [DVC](https://dvc.org/) for managing data, creating, and running pipelines.

Usage

```
cd examples/titanic
dvc pull
dvc repro step_2.csv.dvc
```

To clean-up data files

```
dvc remove -o *.dvc
```

## Documentation

`ayx-learn` follows the [Alteryx Python Documentation Standards](https://alteryx.quip.com/bFgiAZThHaJv/Python-Documentation-Standards).

See [README](docs/README.md).


