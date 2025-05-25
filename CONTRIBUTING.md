# Contributing to Payment Gateway System

Thank you for your interest in contributing to the Payment Gateway System! We appreciate your time and effort in helping us improve this project.

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/payment-gateway.git
   cd payment-gateway
   ```
3. **Set up the development environment** (see [README.md](README.md) for details).
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make your changes** and commit them with a clear, descriptive message.
6. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a pull request** against the `main` branch of the original repository.

## Development Setup

1. **Install dependencies**:
   ```bash
   make install
   ```

2. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

3. **Run tests**:
   ```bash
   make test
   ```

4. **Run the application**:
   ```bash
   make run
   ```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use [Black](https://black.readthedocs.io/) for code formatting.
- Use [isort](https://pycqa.github.io/isort/) for import sorting.
- Use [Flake8](https://flake8.pycqa.org/) for linting.
- Use [mypy](http://mypy-lang.org/) for static type checking.

## Testing

- Write unit tests for new features and bug fixes.
- Run tests with `make test`.
- Ensure all tests pass before submitting a pull request.
- Add integration tests for API endpoints.

## Documentation

- Update the README.md with any changes to setup or usage.
- Add docstrings to all public functions and classes.
- Update any relevant documentation in the `docs/` directory.

## Pull Request Process

1. Ensure your code follows the project's style guidelines.
2. Update the README.md with details of changes if necessary.
3. Ensure all tests pass.
4. Reference any related issues in your pull request description.
5. Wait for the maintainers to review your pull request.

## Reporting Issues

When reporting issues, please include:

- A clear, descriptive title.
- Steps to reproduce the issue.
- Expected vs. actual behavior.
- Any relevant error messages or logs.
- Your environment (OS, Python version, etc.).

## License

By contributing, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.
