
# Contributing to PyFreeform

Help improve the library!

## Development Setup

```bash
# Clone repository
git clone https://github.com/anthropics/pyfreeform.git
cd pyfreeform

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black mypy
```

![Development workflow stages from clone to PR](./_images/06-contributing/01-development-workflow.svg)

## Running Tests

```bash
pytest tests/
```

![Testing pyramid: unit, component, and integration tests](./_images/06-contributing/05-testing-pyramid.svg)

## Code Style

- **Black** for formatting: `black .`
- **Type hints** for public APIs
- **Docstrings** for all public methods

![Code quality tools: Black, MyPy, and Pytest](./_images/06-contributing/02-code-quality-tools.svg)

![Code style guidelines: naming conventions, formatting rules, and documentation standards](./_images/06-contributing/07-code-style-guidelines.svg)

## Areas for Contribution

- New entity types
- Additional shape helpers
- More parametric curves
- Performance improvements
- Documentation
- Examples

![Contribution areas: entities, shapes, curves, performance, docs, examples](./_images/06-contributing/03-contribution-areas.svg)

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure tests pass
5. Submit PR with clear description

![Pull request process with progressive complexity](./_images/06-contributing/04-pull-request-process.svg)

![Git branching strategy: main branch with feature branches](./_images/06-contributing/06-git-branch-strategy.svg)

## See Also
- [Architecture](01-architecture.md)
- [Entity System](02-entity-system.md)
