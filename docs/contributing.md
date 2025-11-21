# Contributing

Thank you for your interest in contributing to AshMatics Core DataModels!

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AsherInformatics/ashmatics-core-datamodels.git
   cd ashmatics-core-datamodels
   ```

2. **Install with development dependencies:**
   ```bash
   uv pip install -e ".[dev,docs]"
   ```

3. **Verify installation:**
   ```bash
   pytest
   ruff check src/
   mypy src/
   ```

## Code Standards

### Pydantic Models
- All models must inherit from `AshMaticsBaseModel`
- Use type hints for all fields
- Include docstrings for classes and non-obvious fields
- Add validators where appropriate

### Validation Philosophy
- **Strict validation** - Fail fast with clear error messages
- **Normalization** - Auto-uppercase codes, trim strings
- **Format checking** - Use regex for identifier patterns

### File Headers
All files must include the Apache 2.0 license header:

```python
# Copyright 2025 Asher Informatics PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# ...
```

## Testing

### Writing Tests
- Test files mirror source structure: `tests/fda/test_clearances.py`
- Test validation edge cases
- Test JSON serialization roundtrips
- Use descriptive test names

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src/ashmatics_datamodels --cov-report=term-missing

# Specific module
pytest tests/fda/

# Specific test
pytest tests/fda/test_clearances.py::TestFDA510kClearance::test_k_number_validation
```

## Code Quality

### Linting
```bash
# Check code
ruff check src/ tests/

# Auto-fix
ruff check --fix src/ tests/

# Format
ruff format src/ tests/
```

### Type Checking
```bash
mypy src/
```

## Documentation

### Building Docs Locally
```bash
# Serve docs locally
mkdocs serve

# Open http://127.0.0.1:8000 in browser

# Build static site
mkdocs build
```

### Adding Documentation
- Add module docs to `docs/modules/`
- Add examples to `docs/examples/`
- Update navigation in `mkdocs.yml`

## Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Add tests for new functionality
   - Update documentation
   - Ensure all tests pass

3. **Commit with clear messages:**
   ```bash
   git commit -m "feat(fda): Add recall severity enum"
   ```

4. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Versioning

We follow [Semantic Versioning](https://semver.org/):

- **Patch (0.X.Y)** - Bug fixes, clarifications
- **Minor (0.X.0)** - New schemas, backward-compatible additions
- **Major (X.0.0)** - Breaking changes to existing schemas

Update both:
- `pyproject.toml` version
- `src/ashmatics_datamodels/__init__.py` `__version__`

## Questions?

Contact: info@asherinformatics.com
