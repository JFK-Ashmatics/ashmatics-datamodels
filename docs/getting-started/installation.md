# Installation

## Requirements

- Python 3.11 or higher
- pip or uv package manager

## Installation Methods

### From Git (Recommended for now)

Install directly from the GitHub repository:

```bash
pip install git+https://github.com/AsherInformatics/ashmatics-core-datamodels.git
```

### Using uv

If you're using [uv](https://github.com/astral-sh/uv):

```bash
uv pip install git+https://github.com/AsherInformatics/ashmatics-core-datamodels.git
```

### Add to pyproject.toml

For projects using `pyproject.toml`:

```toml
[project]
dependencies = [
    "ashmatics-datamodels @ git+https://github.com/AsherInformatics/ashmatics-core-datamodels.git",
]
```

Then install with:

```bash
pip install -e .
# or
uv pip install -e .
```

## Development Installation

To contribute or develop with the library:

```bash
# Clone the repository
git clone https://github.com/AsherInformatics/ashmatics-core-datamodels.git
cd ashmatics-core-datamodels

# Install with development dependencies
pip install -e ".[dev]"

# Or with uv
uv pip install -e ".[dev]"
```

This installs:
- pytest for testing
- pytest-cov for coverage reporting
- ruff for linting
- mypy for type checking

## Documentation Setup (Optional)

To build documentation locally:

```bash
pip install -e ".[docs]"
# or
uv pip install -e ".[docs]"
```

This installs:
- mkdocs
- mkdocs-material theme
- mkdocstrings for API docs
- pymdown-extensions

## Verify Installation

Test your installation:

```python
# In a Python shell
>>> from ashmatics_datamodels import __version__
>>> print(__version__)
'0.2.0'

>>> from ashmatics_datamodels.fda import FDA_510kClearance
>>> clearance = FDA_510kClearance(
...     k_number="K240001",
...     device_name="Test Device",
...     clearance_date="2024-01-15"
... )
>>> print(clearance.k_number)
'K240001'
```

## Next Steps

Now that you have the library installed, proceed to the [Quick Start Guide](quickstart.md) to start using it.
